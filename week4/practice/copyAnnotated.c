/*
Takes in a bmp file
and copies it to a new file
*/

#include <stdio.h>
#include <stdlib.h> // abs()

#include "bmp.h" // bmp structs

int get_padding(int width,int pixel_size);

int main(int argc, char* argv[])
{

    //------------------------------------//
    //~*~*~*~*VALIDATE USER INPUTS*~*~*~*~//
    //-----CREATE READ/WRITE POINTERS-----//

    // user entered correct number of arguments
    if (argc != 3)
    {
        printf("Correct usage: <infile> <outfile>\n");
        return 1;
    }
    //printf("%s %s %s\n", argv[0], argv[1], argv[2]);

    // NAME OUR USER INPUT ARGUMENTS
    char* input_file_name = argv[1];
    char* output_file_name = argv[2];

    // create infile pointer and check if valid

    FILE* input_file_pointer = fopen(input_file_name, "r");
    if (input_file_pointer == NULL)
    {
        printf("File not found, please use a valid file to copy\n");
        return 2;
    }

    // create the outfile pointer while we're at it
    FILE* output_file_pointer = fopen(output_file_name, "w");
    if (output_file_pointer == NULL)
    {
        printf("File could not be created!\n");
        return 3;
    }

    //------------------------------------//
    //~*~*~*~*~READ/WRITE HEADERS*~*~*~*~*//
    //------------------------------------//

    // create a variable to hold our first struct from bmp.h

    BITMAPFILEHEADER bm_header;

    /*
    our input pointer is at the beginning of the file
    where this data lives. We have to pull in the correct
    number of bytes using sizeof(). We only have to pull it
    in 1 time.
    */

    // fread(destination, size of 1 element, # of elements, source)

    fread(&bm_header, sizeof(BITMAPFILEHEADER), 1, input_file_pointer);

    /*
    we've taken data from the infile and put it in a variable
    which we can use to write to our new outfile
    */

    // fwrite(source, size of 1 element, # of elements, destination)

    fwrite(&bm_header, sizeof(BITMAPFILEHEADER), 1, output_file_pointer);


    /*
    next we'll repeat this process for the file info section
    (it's called file info header but we already did the header
    and that makes things less clear)
    */

    BITMAPINFOHEADER bm_file_info;

    // pull info from input into our variable
    fread(&bm_file_info, sizeof(BITMAPINFOHEADER), 1, input_file_pointer);

    // push info from our variable to our output
    fwrite(&bm_file_info, sizeof(BITMAPINFOHEADER), 1, output_file_pointer);



    // now the confusing part...


    /*
    At this point the input pointer has moved along without us
    having to think about it. Imagine a video on youtube just playing
    along. Now what if the video you were watching had a part you wanted
    to skip over. You would click on the small bar below the video
    to skip over a section. We have to do that in a way here for our
    image copy program. We want to skip over the padding and then
    add it back in ourselves manually. This will be a more useful
    technique when we have to resize the image.
    */

    /*
    in bmp.h we have a struct that represents a single pixel
    this is the RGBTRIPLE struct.
    We need to know how many are in a single scanline
    and how many total rows exist in the image.
    We can find out the number of pixels for the width
    and height by accessing those values in the
    BITMAPHEADERINFO struct we read into.
    */

    /*
    To make things more complicated we have to add padding
    which is an arbitrary byte of zeros represented as 0x00.
    We're given the formula for padding so let's hide all that
    mess in a function so we don't have to think about it.
    get_padding() is all we need to know.
    */

    /*
    To make things EVEN MORE COMPLICATED
    the height in some files is negative which is another issue
    we have to solve. Luckily we just have to get the absolute value
    which will turn -42 into 42. We'll use our abs() function for this
    */

    // ONWARD!!!!!!



    // Get all our values ready for looping

    int width = bm_file_info.biWidth;
    int height = abs(bm_file_info.biHeight);
    int padding = get_padding(width, sizeof(RGBTRIPLE));

    // uncomment and try without the abs() to see what it does!
    // printf("height is %d and padding is %d\n", height, padding);


    /*
    This is not so different from the headers, because we're just
    reading a struct and writing it out.
    We have to think about
    rows and columns which means a nested loop.
    draw on a piece of paper a row of 4 little boxes
    then make 2 more rows so you end up with this:
    [] [] [] []
    [] [] [] []
    [] [] [] []
    we have to loop through left to right the width of the matrix
    then the height. So our first loop is the height because we START
    with Row 1 Column 1 then Row 1 Column 2 etc etc.
    There will be padding that needs to be added before we
    loop to the next row. So that part lives under the loop
    that goes through each pixel in a single row. More on that later
    */

    // Create a variable to hold a single pixel
    RGBTRIPLE pixel;

    // LOOPING!

    // outer loop goes to each row
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            /*
            there is no need to keep track of our pointer
            for these reads because the pointer moves on
            to the next pixel each time we run
            the fread() function
            */

            // read it into our variable
            fread(&pixel, sizeof(RGBTRIPLE), 1, input_file_pointer);

            // write it out from our variable
            fwrite(&pixel, sizeof(RGBTRIPLE), 1, output_file_pointer);

        }

        /*
        THIS IS THE YOUTUBE-esque skipping part!
        We want the input point to skip over the padding
        so the outer loop brings us right to the next row
        of pixels.
        Then we want to manually add padding to our output file
        so everyone is on the same page when reading and writing.
        Remember we are keeping track of 2 pointers here. Draw
        those squares and draw a little "I" and "O" on each little
        square. At the end of the row draw a few squiggly lines for
        padding:
        [IO] [] [] [] }}}
        When we do an fread, the I moves
        [O] [I] [] [] }}}
        When we do an fwrite, the O moves
        [] [OI] [] [] }}}
        once we get to the end we're going to manually skip the Input
        over the padding and which will put it right where it needs to be
        to write the next RGBTRIPLE. Then we will manually add the padding
        to our Output so it keeps in line with the input.
        int fseek(pointer, offset, reference point)
        - pointer is the file pointer we want to manipulate
        - offset means by how much (positive numbers go forward
        negative numbers send it backward)
        - fseek has 3 options for the reference point, which means:
        you can move from where the pointer currently is in your
        program (SEEK_CUR)
        you can move based on the very beginning of the file
        (SEEK_SET)
        you can move based on the very end of the file
        (SEEK_END)
        We'll be using SEEK_CUR here
        */


        // move the input pointer ahead, past row (scanline) of padding
        fseek(input_file_pointer, padding, SEEK_CUR);


        /*
        now we add the same amount of padding in a loop to the
        output. Padding is just a byte of zeros so in hex this is
        represented as 0x00. So we'll write 0x00 <padding variable>
        number of times.
        Because our value is exactly the size of a char we can use
        the simpler fputc() function
        fputc(char sized value, destination);
        - char sized value is any char sized value like our 0x00
        - destination is the pointer we want to use, in this case
        put that char in the output pointer!
        NOTE: no quotations when adding hex values
        wrong: "0x00"
        right: 0x00
        For more on how hex values work in C check this out:
        https://tinyurl.com/yc7vdp5e
        */


        for(int k = 0; k < padding; k++)
        {
            fputc(0x00, output_file_pointer);
        }

    }


    /*
    Close the streams for our input and output pointers. This
    frees up any unused resources back to our system.
    */

    fclose(input_file_pointer);

    fclose(output_file_pointer);


    return 0;
}




// helper functions

int get_padding(int width, int pixel_size)
{
    return ( 4 - ( width * pixel_size ) %4 ) % 4;
}