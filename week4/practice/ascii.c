#include <stdio.h>

int main(void)
{
   int s = 65;
   int* t = &s;

   // TODO: Print "POINTER" using these chars

   char C = 'I'; //I
   char N = s + 'P' - 'A'; // P
   char B = *t - s + N + 2; // R
   char E = &s - t + 78; // N
   char J = *t + 19; // T
   char I = N + 'A' - s - 1; // O
   char O = 347/5; // E

   printf("%c%c%c%c%c%c%c\n", N, I, C, E, J, O, B);
}