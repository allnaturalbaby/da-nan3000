#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <syslog.h>

#define LOKAL_PORT 80
#define BAK_LOGG 10 // Størrelse på for kø ventende forespørsler

const char *getFileType(const char *fileName)
{
  const char *dot = strrchr(fileName, '.');
  if (!dot || dot == fileName)
    return "";
  return dot + 1;
}

int readAsis(char *fileName)
{
  FILE *fptr;
  char asisPath[100] = "./asis";

  char c;
  const char *fileType = getFileType(fileName);

  strcat(asisPath, fileName);

  fptr = fopen(asisPath, "r");

  if (strlen(fileName) > 1 && strcmp(fileType, "asis") != 0)
  {
    if (fptr == NULL)
    {
      // handle error (path doesnt exist)
      printf("%s", "404 Not Found");
      exit(0);
    }

    printf("%s", "415 Unsupported Media Type.");
    exit(0);
  }

  if (fptr == NULL)
  {
    // handle error (path doesnt exist)
    printf("%s", "404 Not Found");
    exit(0);
  }

  c = fgetc(fptr);
  while (c != EOF)
  {
    printf("%c", c);
    c = fgetc(fptr);
  }
  fclose(fptr);
  return 0;
}

void handleHttpRequest(int sd)
{
  const int request_buffer_size = 65536;
  char request[request_buffer_size];

  int bytes_recvd = recv(sd, request, request_buffer_size - 1, 0);

  if (bytes_recvd < 0)
  {
    perror("revc");
    return;
  }

  char *requestType;
  requestType = strtok(request, " ");
  char *path;
  path = strtok(NULL, " ");

  if (strlen(path) >= 1) // not needed?
  {
    //printf("%s", path);
    readAsis(path);
  }
}

static void skelly_daemon(){
    pid_t pid;
    pid = fork();
    
    if (pid < 0){
        exit(EXIT_FAILURE);
    }

    if (pid > 0){
        exit(EXIT_SUCCESS);
    }

    if (setsid() < 0){
        exit(EXIT_FAILURE);
    }

    signal(SIGCHLD, SIG_IGN);
    signal(SIGHUP, SIG_IGN);

    pid = fork();

    if (pid < 0){
        exit(EXIT_FAILURE);
    }

    if (pid > 0){
        exit(EXIT_SUCCESS);
    }

    umask(0); //fakking up?

    chroot("var/www/mp1");

    int x;
    for (x=sysconf(_SC_OPEN_MAX); x>=0; x--){
        close(x);
    }
}

int privilege(){

    uid_t uid = 1000;
    gid_t gid = 1000;

    if (getuid() == 0) {
        setuid(uid);
        setgid(gid);
    }

    if (setuid(0) != -1){
        exit(0);
    }
}

int web_service(){
  struct sockaddr_in lok_adr;
  int sd, ny_sd;

  // Setter opp socket-strukturen
  sd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

  // For at operativsystemet ikke skal holde porten reservert etter tjenerens død
  setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, &(int){1}, sizeof(int));

  // Initierer lokal adresse
  lok_adr.sin_family = AF_INET;
  lok_adr.sin_port = htons((u_short)LOKAL_PORT);
  lok_adr.sin_addr.s_addr = htonl(INADDR_ANY);

  // Kobler sammen socket og lokal adresse
  if (0 == bind(sd, (struct sockaddr *)&lok_adr, sizeof(lok_adr)))
    fprintf(stderr, "Prosess %d er knyttet til port %d.\n", getpid(), LOKAL_PORT);
  else
    exit(1);

  privilege();//root drit

  // Venter på forespørsel om forbindelse
  listen(sd, BAK_LOGG);
  while (1)
  {

    // Aksepterer mottatt forespørsel
    ny_sd = accept(sd, NULL, NULL);

    if (0 == fork())
    {

      dup2(ny_sd, 1); // redirigerer socket til standard utgang

      handleHttpRequest(ny_sd);

      fflush(stdout);

      // Sørger for å stenge socket for skriving og lesing
      // NB! Frigjør ingen plass i fildeskriptortabellen
      shutdown(ny_sd, SHUT_RDWR);
      exit(0);
    }

    else
    {
      close(ny_sd);
    }
  }
  return 0;
}

int main(){
    skelly_daemon();

    while(1){
        web_service();
    }
}