#include <stdio.h>
#include <cs50.h>

int main (void)
{
    char* str = get_string("Enter string: ");
    int counter = 0;

    for (char* ptr = str; *ptr != '\0'; ptr ++)
    {
        counter++;
    }

    printf("%d\n", counter);
}