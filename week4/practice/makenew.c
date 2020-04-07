#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Usage: ./makefile filename filetext");
        return 1;
    }

    char * filename = argv[1];
    char * text = argv[2];

    /*printf("%s\n", filename);
    for (int i = 0; i < strlen(text); i++)
    {
        printf("%c\n", text[i]);
    }*/
    FILE * inptr;
    inptr = fopen(filename, "w");

    fwrite(text, sizeof(text[0]), sizeof(text), inptr);
    fclose(inptr);
    return 0;

}