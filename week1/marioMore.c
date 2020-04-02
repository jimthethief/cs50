#include <cs50.h>
#include <stdio.h>

void printLoop(string, int);

int main(void)
{
    int height;

    //ask for input and make sure it is between 1 & 8
    do {
        height = get_int("Height: ");
    }
    while (height <= 0 || height > 8);
    
    //declare starting values of hash and space
    int space = height - 1;
    int hash = 1;
    
    //draw pyramid
    for (int i = 0; i < height; i++) {
        printLoop(" ", space);
        printLoop("#", hash);
        printf("  ");
        printLoop("#", hash);
        printf("\n");
        space--;
        hash++;
    }
}

//define printLoop function - takes str and prints num times
void printLoop(string str, int num) {
    for (int i = 0; i < num; i++) {
        printf("%s", str);
    }
}