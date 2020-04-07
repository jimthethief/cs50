#include <stdio.h>
#include <cs50.h>
#include <ctype.h>

void swap(int* a, int* b)
{
                       // a = 1; b = 2; tmp = NULL;
    int tmp = *a;     // store *a in tmp a = 1; b = 2; tmp = 1;
    *a = *b;         // assign *a to *b a = 2; b = 2; tmp = 1;
    *b = tmp;       // assign tmp to *b a = 2; b = 1; tmp = 1;
}

int main(void)
{
    int x = get_int("Enter integer A: ");
    int y = get_int("Enter integer B: ");
    printf("A is %i\n", x);
    printf("B is %i\n", y);
    printf("Would you like to swap integer A with integer B?\n");
    char ans = 'a';
    while (ans != 'Y' || ans != 'N')
    {
        ans = get_char("Please enter Y or N: ");
        ans = toupper((unsigned char) ans);

        if (ans == 'N')
        {
            printf("A and B were not swapped.\n");
            printf("A is still %i\n", x);
            printf("B is still %i\n", y);
            return 1;
        }
        else if (ans == 'Y')
        {
            printf("Swapping...\n");
            swap(&x, &y);
            printf("Swapped!\n");
            printf("A is %i\n", x);
            printf("B is %i\n", y);
            return 0;
        }
    }
}