#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>


#define BLOCK_SIZE 512
typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover filename\n");
        return 1;
    }

    // remember filename
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }


    /* READING THE FILE

    fread(data, size, number, inptr);

    - data: pointer to a 'struct' that will contain the bytes you're reading
    - size: size of each element to read... sizeof()
    - number: number of elements to read
    - inptr: FILE * to read from

    fread returns the number of elements successfully read

    fread(buffer, 1, 512, raw_file); // reads 1 block of 512 bytes at a time
    fread(buffer, 512, 1, raw_file); // reads 512 blocks 1 byte each

    */

    // create buffer
    BYTE buffer[BLOCK_SIZE];

    // counter for JPEG
    int jpgCount = 0;

    // check if jpg is found
    bool foundJPG = false;

    // create pointer for new img file
    FILE *img = NULL;

    // char array to store the resultant string
    char filename[8]; // [8] because "000.jpg" + \0

    while (fread(buffer, BLOCK_SIZE, 1, inptr) == 1)
    {
        // identifying a JPEG:
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xe0) == 0xe0)
        {
            // close img from previous iteration & add to jpegCount
            if (foundJPG == true)
            {
                fclose(img);
            }
            else
            {
                foundJPG = true;
            }

            // name new file
            sprintf(filename, "%03i.jpg", jpgCount);

            //open file for writing
            img = fopen(filename, "w");
            jpgCount++;

        }
        // skip if first jpg file is not found
        if (foundJPG == true)
        {
            fwrite(&buffer, BLOCK_SIZE, 1, img);
            // check file creation is successful
            if (img == NULL)
            {
                fclose(inptr);
                free(buffer);
                fprintf(stderr, "Could not create output file for %s.\n", filename);
                return 3;
            }
        }
    }

    // close open files and free buffer
    fclose(inptr);
    fclose(img);

    return 0;
}
