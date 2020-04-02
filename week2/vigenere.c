#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int shift(char c);
char encode(char letter, int lock);

int main(int argc, string argv[])
{
    // check only 2 arguments
    if (argc == 2)
    {
        //iterate through 2nd argument and check all chars are digits
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (isalpha(argv[1][i]) == 0)
            {
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
        }
        string plain = get_string("plaintext: ");
        printf("ciphertext: ");
        // set amount of 
        int shiftBy = -1;
        for (int i = 0; i < strlen(plain); i++)
        {
            // reset keyIndex tracker to 0
            int keyIndex = 0;
            if (shiftBy < (strlen(argv[1]) - 1))
            {
                // increase shiftBy by 1 and add to keyIndex tracker
                // if shiftBy < n(strlenargv[1]) - 1  
                shiftBy++;                
                keyIndex += shiftBy;
            }
            else 
            {
                // reset counters to 0 when counter reaches argument length
                keyIndex = 0;
                shiftBy = 0;
            }
            int key = shift(argv[1][keyIndex]);
            // check character is a letter and encode if it is
            if ((plain[i] >= 'a' && plain[i] <= 'z') || (plain[i] >= 'A' && plain[i] <= 'Z'))
            {
                printf("%c", encode(plain[i], key)); // print character using encode function
            }
            else 
            {
                // print character unciphered if it isn't a letter
                printf("%c", plain[i]);
                shiftBy--;
                keyIndex -= shiftBy;
            }
        }
        printf("\n");
        return 0;
    }
    else 
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
}

int shift(char c)
{
    // check if upper or lowercase - A is less than a
    if (c >= 'a')
    {
        int shifted = c - 'a';
        return shifted;
    }
    else
    {
        int shifted = c - 'A';
        return shifted;
    }
}

char encode(char letter, int lock)
{
    // check if upper or lowercase - A is less than a
    if (letter >= 'a')
    {
        // subtract value of a from letter and add key
        // if value is > 26, remainder causes cipher to 'loop back' to a
        // add 0 - 26 value to value of a to get ciphered char
        char ciphered = (((letter - 'a') + lock) % 26) + 'a';
        return ciphered; 
    }
    else 
    {
        char ciphered = (((letter - 'A') + lock) % 26) + 'A';
        return ciphered;
    }
}