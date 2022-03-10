#include "headers.h"
#include <arpa/inet.h>
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
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

char *getResponseHeaderFromExtension(char *extension) {
    if (strcmp(extension, "html") == 0 || strcmp(extension, "htm") == 0) {
        return text_html;
    }
    if (strcmp(extension, "jpeg") == 0) {
        return image_jpeg;
    }
    if (strcmp(extension, "txt") == 0) {
        return text_plain;
    }
    if (strcmp(extension, "gif") == 0) {
        return image_gif;
    }
    if (strcmp(extension, "css") == 0) {
        return text_css;
    }
    if (strcmp(extension, "xml") == 0) {
        return application_xml;
    }
    if (strcmp(extension, "json") == 0) {
        return application_json;
    }
    return "";
}

char *isFileExtensionAllowed(char *fileExt) {
    char *buf = NULL;
    char *p = NULL;

    size_t length = 0;
    int count = 0;

    FILE *mimeFile;
    char *mimeType;

    mimeFile = fopen("/mimetypes/mime.types", "r");

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
            mimeType = p;

            while (0 != (p = strtok(NULL, "\t "))) {
                if (strcmp(fileExt, p) == 0) {
                    // logger(mimeType, 2);
                    return mimeType;
                }
            }
        }
        // fclose(mimeFile);
    } else {
        logger("nopp", 2);
    }
    // free(buf);
    return NULL;
}

char *getFileType(char *fileName) {
    char *dot = strrchr(fileName, '.');
    if (!dot || dot == fileName)
        return "";
    return dot + 1;
}

int readFilePath(char *fileName, int sd) {
    FILE *fptr;
    char pagesPath[100] = "/pages";
    char response[BUFSIZ];

    struct stat statbuf;

    char c;
    char *fileType = getFileType(fileName);

    char *contentType = getResponseHeaderFromExtension(fileType);

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
        contentType = bad_request;
        fptr = fopen("/response/404.html", "r");
        logger("Code 404", 0);
    }

    if (stat(pagesPath, &statbuf) == 0 && strlen(fileName) > 1) {
        if (strcmp(fileType, "asis") != 0 && isFileExtensionAllowed(fileType) == NULL) {
            if (fptr == NULL) {
                // 404 error handling
                contentType = bad_request;
                fptr = fopen("/response/404.html", "r");
                logger("Code 404", 0);
            } else {
                // 415 error handling
                contentType = unsupported_type;
                fptr = fopen("/response/415.html", "r");
                logger("Code 415", 0);
            }
        }
    }

    if (strcmp(fileType, "jpeg") == 0 || strcmp(fileType, "png") == 0 || strcmp(fileType, "jpg") == 0 || strcmp(fileType, "gif") == 0) {
        send(sd, contentType, strlen(contentType), 0); // sends the appropriate header
        while (fread(response, 1, sizeof(response), fptr) != 0) {
            send(sd, response, sizeof(response), 0);
        }
    } else {
        send(sd, contentType, strlen(contentType), 0); // sends the appropriate header
        while (fgets(response, BUFSIZ, fptr) != NULL) {
            send(sd, response, strlen(response), 0);
        }
    }

    fclose(fptr);

    return 0;
}

void handleHttpRequest(int sd) {
    const int request_buffer_size = 65536;
    char request[request_buffer_size];
    char response[BUFSIZ];

    int bytes_recvd = recv(sd, request, request_buffer_size - 1, 0);

    if (bytes_recvd < 0) {
        logger("No bytes recieved.", 0);
        return;
    }

    char *requestType;
    requestType = strtok(request, " ");
    char *path;
    path = strtok(NULL, " ");

    FILE *fptr = fopen("./index.html", "r");

    if (strlen(path) >= 1) {
        readFilePath(path, sd);
    } else {
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

    umask(0); // set new file permissions

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

    int errVal = chroot("/var/www/");
    if (errVal < 0) {
        perror("/var/www/mp2/");
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

int main() {         // the magic
    skelly_daemon(); // starter daemoniseringen av programmet

    while (1) {
        web_service(); // starter webtjenesten
    }
}