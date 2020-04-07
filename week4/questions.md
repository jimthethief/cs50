# Questions

## What's `stdint.h`?

A header file in the C standard library. It was introduced to allow programmers to write more portable code by providing a set of typedefs that specify exact-width integer types. This is useful to get a program working universally across different systems. [Source](https://en.wikibooks.org/wiki/C_Programming/stdint.h)

*In other words - you might not always want to rely on standard data types in C like int or double. When you include stdint.h header file you can define new integer types of more specific sizes.*

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

All of these definitions are exact width integers for cross-platform implementation of a standard data type:

- **uint8_t**
    - An unsigned 8 bit 'width' integer ```__int8```, the range is from 0 to 255 decimal.
    
- **uint16_t**
    - An unsigned 16 bit integer, the range is from 0 to 65535 decimal.
    
- **uint32_t**
    - An unsigned 32 bit integer, the range is from 0 to 4294967295 decimal.
    
- **int32_t**
    - A 32-bit signed integer, has a range of –2147483648 to 2147483647 decimal. The first bit (MSB) is the signing bit. This type can be specified as unsigned by using the unsigned data-type modifier (see above).

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

- **BYTE:** 1
- **DWORD:** 4
- **LONG:** 4
- **WORD:** 2

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The header field used to identify the BMP file is `0x42 0x4D` in hexadecimal, which is the same as `BM` in ASCII.

## What's the difference between `bfSize` and `biSize`?

- **bfSize** is the size, in bytes, of the bitmap file.
- **biSize** is the number of bytes required by the structure.

## What does it mean if `biHeight` is negative?

*biHeight* is the height of the bitmap, in pixels. If biHeight is negative, the bitmap is a top-down DIB (<< another term for bitmap file) and its origin is the upper-left corner. 

(If biHeight is positive, the bitmap is a bottom-up DIB and its origin is the lower-left corner.)

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

The *biBitCount* specifies the number of bits-per-pixel. It determines the number of bits that define each pixel and the maximum number of colors in the bitmap.

## Why might `fopen` return `NULL` in `copy.c`?

Will return `NULL` if the file cannot be opened. E.g. there isn't enough memory or the file cannot be found

## Why is the third argument to `fread` always `1` in our code?

`1` specifies the number of elements being read at a time by `fread`. The file is being read pixel by pixel, so this stays as 1 for the purposes of `copy.c`.

## What value does `copy.c` assign to `padding` if `bi.biWidth` is `3`?

`copy.c` would assign `padding` a value of **3**.
 - RGBTRIPLE = 3
 - bi.biWidth = 3
     int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

## What does `fseek` do?

The fseek() function changes the current file position associated with stream to a new location within the file. The next operation on the stream takes place at the new location. On a stream opened for update, the next operation can be either a reading or a writing operation. [source] (https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.4.0/com.ibm.zos.v2r4.bpxbd00/fseek.htm)

The origin must be one of the following constants defined in stdio.h:
- **SEEK_SET:** Beginning of file
- **SEEK_CUR:** Current position of file pointer
- **SEEK_END:** End of file

For copy.c this means skipping over the padding int and moving the file pointer position to the location of the next triple with `SEEK_CUR`.

## What is `SEEK_CUR`?

`SEEK_CUR` is the current position of file pointer
