#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
int err(char *error_string){
    FILE *err_file = fopen("log.txt", "a");
    dup2(fileno(err_file), STDERR_FILENO);
    fprintf(stderr, error_string);
    fprintf(stderr, "\n");
    fclose(err_file);
}

int main(){
    err("Something");
}