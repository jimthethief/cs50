#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    // check only 2 arguments
    if(argc == 2)
    {
        //iterate through 2nd argument and check all chars are digits
        for(int i = 0; i < strlen(argv[1]); i++)
        {
            if(isdigit(argv[1][i]) == 0)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        
        // convert argument from string to integer
        int key = atoi(argv[1]);
        
        string plain = get_string("plaintext: ");
        printf("ciphertext: ");
        
        // print ciphered text
        for(int i = 0; i < strlen(plain); i++)
        {
            if((plain[i] >= 'a' && plain[i] <= 'z') || (plain[i] >= 'A' && plain[i] <= 'Z'))
            {
                printf("%c", plain[i] + key);
            }
            else printf("%c", plain[i]);
        }
        printf("\n");
        return 0;
    }
    else printf("Usage: ./caesar key\n");
}