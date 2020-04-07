// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: integer infile outfile\n");
        return 1;
    }

    // remember filenames & integer
    int n = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    if (n < 1  || n > 100)
    {
        fprintf(stderr, "Ensure that your integer is > 0 and <= 100\n");
        return 1;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // create outfile header variables
    BITMAPFILEHEADER outbf;
    BITMAPINFOHEADER outbi;

    // make copy of input headers int output variable
    outbf = bf;
    outbi = bi;

    // amending outfile BITMAPFILEHEADER and BITMAPINFOHEADER by factor of n
    outbi.biWidth *= n;
    outbi.biHeight *= n;

    // determine padding for scanlines
    int inPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int outPadding = (4 - (outbi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;


    // scale image using amended biWidth and biHeight values
    outbi.biSizeImage = ((sizeof(RGBTRIPLE) * outbi.biWidth) + outPadding) * abs(outbi.biHeight);

    // scale bfSize of outfile so scaled image fits
    outbf.bfSize = outbi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);


    // write outfile's BITMAPFILEHEADER
    fwrite(&outbf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&outbi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // buffer to hold a scanline's worth of pixels:
    RGBTRIPLE *scanline = malloc(sizeof(RGBTRIPLE) * outbi.biWidth);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        int pixelCount = 0;

        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // temporary storage (triple is just a pixel)
            RGBTRIPLE triple;

            // read pixel from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            for (int k = 0; k < n; k++)
            {
                // adding to buffer n number of times
                // use pixelCount to ensure correct placement of pixel
                *(scanline + pixelCount) = triple;
                pixelCount++;
            }

        }

        // skip over padding, if any
        fseek(inptr, inPadding, SEEK_CUR);

        for (int l = 0; l < n; l++)
        {
            // write previously stored scanline of pixels to outfile
            // repeat for n number of rows
            fwrite(scanline, sizeof(RGBTRIPLE), outbi.biWidth, outptr);

            // then add padding back in at end of each row
            for (int m = 0; m < outPadding; m++)
            {
                fputc(0x00, outptr);
            }
        }
    }


    // free scanline's memory alloc

    free(scanline);
    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
