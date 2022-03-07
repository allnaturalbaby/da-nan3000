#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <syslog.h>

#define LOCAL_PORT 80
#define BACK_LOG 10 // Størrelse på for kø ventende forespørsler

int err(char *error_string, int type){
    FILE *err_file = fopen("log.txt", "a");
    dup2(fileno(err_file), STDERR_FILENO);

    if(type == 0){
      fprintf(stderr, "[ERROR]:\t\t");
    }
    if(type == 1){
      fprintf(stderr, "[SUCCESS]:\t");
    }
    if(type == 2) {
      fprintf(stderr, "[INFO]:\t\t");
    }

    fprintf(stderr, error_string);
    fprintf(stderr, "\n");
    fclose(err_file);
}


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
  FILE *response;
  char asisPath[100] = "./asis";

  char c;
  const char *fileType = getFileType(fileName);

  //Send log value
    char *buf;
    size_t sz;
    sz = snprintf(NULL, 0, "Attemting to open file %s", fileName);
    buf = (char *)malloc(sz + 1);
    snprintf(buf, sz+1, "Attemting to open file %s", fileName);

    err(buf, 2);


  strcat(asisPath, fileName);

  fptr = fopen(asisPath, "r");

  if (strlen(fileName) > 1 && strcmp(fileType, "asis") != 0)
  {
    if (fptr == NULL)
    {
      //404 error handling
      fptr = fopen("./response/404.html", "r");
      err("Code 404", 0);
    }
    else{
  //415 error handling
    fptr = fopen("./response/415.html", "r");
    err("Code 415", 0);
    }
  }
  
  //read through file
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
    err("No bytes recieved.", 0);
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

    err("Daemonizing starting", 2);
    pid_t pid;
    pid = fork(); // fork of process
    
    if (pid < 0){ //an error with forking
        err("Forking failed", 0);
        exit(EXIT_FAILURE);
    }

    if (pid > 0){ //terminate parent
        exit(EXIT_SUCCESS);
    }

    if (setsid() < 0){ //set child as session leader
        err("Set id failed", 0);
        exit(EXIT_FAILURE);
    }

    pid = fork();//fork a second time

    if (pid < 0){
        err("Forking failed", 0);
        exit(EXIT_FAILURE); //error
    }

    if (pid > 0){
        exit(EXIT_SUCCESS); //terminate parent
    }

    umask(0); //set new file permissions

    chroot("var/www/mp1"); //change directory

    int x;
    for (x=sysconf(_SC_OPEN_MAX); x>=0; x--){ //close all file descriptors
        close(x);
    }

    err("Daemon running", 1);
}


int privilege(){

    uid_t uid = 1000; //set user and grup to main user
    gid_t gid = 1000; //should have sepearte service user for security

    if (getuid() == 0) { //check if root
        setuid(uid); //set as user
        setgid(gid);
    }

    if (setuid(0) != -1){ //check possibility to regain root
        err("Regained root permissions, exiting...", 0);
        exit(0); //exit if possible
        
    }

    err("Privilege seperation complete!", 1);
}


int web_service(){
  err("Starting web server", 2);
  struct sockaddr_in lok_adr;
  int sd, ny_sd;
  // Setter opp socket-strukturen
  sd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

  // For at operativsystemet ikke skal holde porten reservert etter tjenerens død
  setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, &(int){1}, sizeof(int));

  // Initierer lokal adresse
  lok_adr.sin_family = AF_INET;
  lok_adr.sin_port = htons((u_short)LOCAL_PORT);
  lok_adr.sin_addr.s_addr = htonl(INADDR_ANY);

  // Kobler sammen socket og lokal adresse
  if (0 == bind(sd, (struct sockaddr *)&lok_adr, sizeof(lok_adr))){

    char *buf;
    size_t sz;
    sz = snprintf(NULL, 0, "Process %d is connected to %d.", getpid(), LOCAL_PORT, 2);
    buf = (char *)malloc(sz + 1);
    snprintf(buf, sz+1, "Process %d is connected to %d.", getpid(), LOCAL_PORT, 2);

    err(buf, 2);

  }
  else
    exit(1);

  privilege();//root seperasjon
  err("Waiting for request", 2);

  // Venter på forespørsel om forbindelse
  listen(sd, BACK_LOG);
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

int main(){ //the magic
  
  skelly_daemon(); //starter daemoniseringen av programmet

  while(1){
      web_service(); // starter webtjenesten
  }
}