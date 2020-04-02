#include <stdio.h>
#include <cs50.h>
#include <math.h> // Included for round function

int main(void) 
{
    // declare variables
    float dollars;
    
    // ask user for float input & check number is positive
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);
    
    
    // use round to convert dollars to cents
    int cents = round(dollars * 100);
    
    // set counters to zero for amount of coins and type of coin

    int coinCounter = 0,
        quarterCounter = 0,
        dimeCounter = 0,
        nickelCounter = 0,
        pennyCounter = 0;
    
    // loop through coin demoninations, checking <= user input in cents
    // add to counter for coin and amount of coins if denomination is used

    while (25 <= cents)
    {
        cents -= 25;
        coinCounter++;
        quarterCounter++;       
    }
    while (10 <= cents)
    {
        cents -= 10;
        coinCounter++;
        dimeCounter++;
    }
    while (5 <= cents) 
    {
        cents -= 5;
        coinCounter++;
        nickelCounter++;
    }
    while (1 <= cents) 
    {
        cents -= 1;
        coinCounter++;
        pennyCounter++;
    }
    
    //print counter to display amount of coins given as change
    printf("Number of coins: %i\n 
            Quarters: %i\n 
            Dimes: %i\n 
            Nickels: %i\n
            Pennies: %i\n", 
            coinCounter, 
            quarterCounter, 
            dimeCounter, 
            nickelCounter, 
            pennyCounter);
}