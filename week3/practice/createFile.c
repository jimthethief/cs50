#include <stdio.h>

int main(void){

    // create file pointer data type fp
    FILE * fp;

    // open file in write mode ("w")
    // remember: fopen returns file pointer for write/read actions
    // this file doesn't exist - fp is just an empty container
    // the container can be filled with fwrite
    fp = fopen("mynewfile.txt", "w");

    // some data for the file in array form:
    char word[] = "array\n";

    // stored as an array ['a', 'r', 'r', 'a', 'y']

    // providing fwrite function with:
    // word variable (array), the size of each element in the array
    // the total number of elements sizeof(word) & the pointer to the file (fp)
    fwrite(word, sizeof(word[0]), sizeof(word), fp);

    fclose(fp);

    return 0;
}