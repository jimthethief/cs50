#include <stdio.h>

int main(void){
    // So I made createFile.c - which passed an array ['a', 'r', 'r', 'a', 'y']
    // into a new file it had created mynewfile.txt

    // lets print this very exciting file to the console

    FILE * fp = fopen("mynewfile.txt", "r"); // "r" is to read a file

    /* ^^ this is the same as:
    FILE * fp;
    fp = fopen("mynewfile.txt", "w");

    from createFile.c */

    // pull in one char at a time using fgetc
    // stop when feof(fp) is true  'break'

    char c;

    while(1) {
        c = fgetc(fp);
        if (feof(fp)) {
        break; // we need to break once feof() returns true
        }

        printf("%c", c);
    }
    fclose(fp);

    return 0;
}