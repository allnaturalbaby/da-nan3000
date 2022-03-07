#include <arpa/inet.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <syslog.h>
#include <unistd.h>

#define LOCAL_PORT 80
#define BACK_LOG 10 // Størrelse på for kø ventende forespørsler

int logger(char *error_string, int type) {
    FILE *err_file = fopen("log.txt", "a");
    dup2(fileno(err_file), STDERR_FILENO);

    if (type == 0) {
        fprintf(stderr, "[ERROR]:\t\t");
    }
    if (type == 1) {
        fprintf(stderr, "[SUCCESS]:\t");
    }
    if (type == 2) {
        fprintf(stderr, "[INFO]:\t\t");
    }

    fprintf(stderr, "%s", error_string);
    fprintf(stderr, "\n");
    fclose(err_file);
}

int isFileExtensionAllowed(char *fileExt) {
    // if (strcmp(fileExt, "ico") == 0) {
    //     return -1;
    // }
    char *buf = NULL;
    char *p = NULL;

    size_t length = 0;
    int count = 0;

    FILE *mimeFile;

    mimeFile = fopen("./mimetypes/mime.types", "r");

    if (mimeFile != NULL) {
        while (0 < (count = getline(&buf, &length, mimeFile))) {
            if (buf[0] == '#') {
                continue;
            }
            if (count < 2) {
                continue;
            }
            buf[count - 1] = '\0';

            p = strtok(buf, "\t ");

            while (0 != (p = strtok(NULL, "\t "))) {
                if (strcmp(fileExt, p) == 0) {
                    logger(p, 2);
                    return 0;
                }
            }
        }
        // fclose(mimeFile);
    } else {
        logger("nopp", 2);
    }
    free(buf);
    return -1;
}

char *getFileType(char *fileName) {
    char *dot = strrchr(fileName, '.');
    if (!dot || dot == fileName)
        return "";
    return dot + 1;
}

int readAsis(char *fileName, int sd) {
    FILE *fptr;
    char pagesPath[100] = "./pages";
    char response[BUFSIZ];

    struct stat statbuf;

    char c;
    char *fileType = getFileType(fileName);

    // Send log value
    char *buf;
    size_t sz;
    if (strcmp(fileType, "ico") != 0) {
        sz = snprintf(NULL, 0, "Attemting to open file %s", fileName);
        buf = (char *)malloc(sz + 1);
        snprintf(buf, sz + 1, "Attemting to open file %s", fileName);

        logger(buf, 2);
    }

    strcat(pagesPath, fileName);

    fptr = fopen(pagesPath, "r");

    if (stat(pagesPath, &statbuf) != 0) {
        fptr = fopen("./response/404.html", "r");
        logger("Code 404", 0);
    }

    if (stat(pagesPath, &statbuf) == 0 && strlen(fileName) > 1) {
        if (strcmp(fileType, "asis") != 0 && isFileExtensionAllowed(fileType) != 0) {
            if (fptr == NULL) {
                // 404 error handling
                fptr = fopen("./response/404.html", "r");
                logger("Code 404", 0);
            } else {
                // 415 error handling
                fptr = fopen("./response/415.html", "r");
                logger("Code 415", 0);
            }
        }
    } else {
        // if (strcmp(fileType, "ico") != 0) {
        fptr = fopen("./response/404.html", "r");
        logger("Code 404", 0);
        //}
    }

    if (strcmp(fileType, "jpeg") == 0 || strcmp(fileType, "png") == 0 || strcmp(fileType, "jpg") == 0 || strcmp(fileType, "gif") == 0) {
        send(sd, response, strlen(response), 0);
        while (fread(response, 1, sizeof(response), fptr) != 0) {
            send(sd, response, sizeof(response), 0);
        }
    } else {
        while (fgets(response, BUFSIZ, fptr) != NULL) {
            send(sd, response, strlen(response), 0);
        }
    }

    // greiene her er for å vise bildefiler

    fclose(fptr);

    return 0;
}

void handleHttpRequest(int sd) {
    const int request_buffer_size = 65536;
    char request[request_buffer_size];

    int bytes_recvd = recv(sd, request, request_buffer_size - 1, 0);

    if (bytes_recvd < 0) {
        logger("No bytes recieved.", 0);
        return;
    }

    char *requestType;
    requestType = strtok(request, " ");
    char *path;
    path = strtok(NULL, " ");

    if (strlen(path) >= 1) // not needed?
    {
        // printf("%s", path);
        readAsis(path, sd);
    }
}

static void skelly_daemon() {

    logger("Daemonizing starting", 2);
    pid_t pid;
    pid = fork(); // fork of process

    if (pid < 0) { // an error with forking
        logger("Forking failed", 0);
        exit(EXIT_FAILURE);
    }

    if (pid > 0) { // terminate parent
        exit(EXIT_SUCCESS);
    }

    if (setsid() < 0) { // set child as session leader
        logger("Set id failed", 0);
        exit(EXIT_FAILURE);
    }

    signal(SIGTTOU, SIG_IGN);
    signal(SIGTTIN, SIG_IGN);
    signal(SIGTSTP, SIG_IGN);
    signal(SIGCHLD, SIG_IGN);

    pid = fork(); // fork a second time

    if (pid < 0) {
        logger("Forking failed", 0);
        exit(EXIT_FAILURE); // error
    }

    if (pid > 0) {
        exit(EXIT_SUCCESS); // terminate parent
    }

    chroot("/var/www/mp2"); // change directory
    umask(0);               // set new file permissions

    for (int x = sysconf(_SC_OPEN_MAX); x >= 0; x--) { // close all file descriptors
        close(x);
    }

    logger("Daemon running", 1);
}

int privilege() {
    uid_t uid = 1000; // set user and grup to main user
    gid_t gid = 1000; // should have sepearte service user for security

    if (getuid() == 0) { // check if root
        if (setgid(gid) != 0) {
            logger("Unable to drop group privileges. Exiting.", 0);
        }; // set as user
        if (setuid(uid) != 0) {
            logger("Unable to drop user privileges. Exiting.", 0);
        }; // set as user
    } else {
        logger("Not root", 2);
    }
    // if (getuid() == 0) { // check if root
    //     setuid(uid);     // set as user
    //     setgid(gid);
    // }

    if (setuid(0) != -1) { // check possibility to regain root
        logger("Regained root permissions, exiting...", 0);
        exit(0); // exit if possible
    }

    logger("Privilege seperation complete!", 1);
}

int web_service() {
    logger("Starting web server", 2);
    struct sockaddr_in lok_adr;
    int sd, ny_sd;
    // Setter opp socket-strukturen
    sd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    char http_request[1024];

    // For at operativsystemet ikke skal holde porten reservert etter tjenerens død
    setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, &(int){1}, sizeof(int));

    // Initierer lokal adresse
    lok_adr.sin_family = AF_INET;
    lok_adr.sin_port = htons((u_short)LOCAL_PORT);
    lok_adr.sin_addr.s_addr = htonl(INADDR_ANY);

    // Kobler sammen socket og lokal adresse
    if (0 == bind(sd, (struct sockaddr *)&lok_adr, sizeof(lok_adr))) {

        char *buf;
        size_t sz;
        sz = snprintf(NULL, 0, "Process %d is connected to %d.", getpid(), LOCAL_PORT);
        buf = (char *)malloc(sz + 1);
        snprintf(buf, sz + 1, "Process %d is connected to %d.", getpid(), LOCAL_PORT);

        logger(buf, 2);

    } else {
        exit(1);
    }

    privilege(); // root seperasjon
    logger("Waiting for request", 2);

    // Venter på forespørsel om forbindelse
    listen(sd, BACK_LOG);
    while (1) {
        // Aksepterer mottatt forespørsel
        ny_sd = accept(sd, NULL, NULL);
        if (fork() == 0) {
            dup2(ny_sd, 1); // redirigerer socket til standard utgang

            handleHttpRequest(ny_sd);

            fflush(stdout);

            // Sørger for å stenge socket for skriving og lesing
            // NB! Frigjør ingen plass i fildeskriptortabellen
            shutdown(ny_sd, SHUT_RDWR);
            exit(0);
        } else {
            close(ny_sd);
        }
    }
    return 0;
}

int main() {                // the magic
    chroot("/var/www/mp2"); // change directory
    skelly_daemon();        // starter daemoniseringen av programmet

    while (1) {
        web_service(); // starter webtjenesten
    }
}