#include <cs50.h>
#include <ctype.h>
#include <stdio.h>

int hash_function(char* key, int size)
{
    int hash = 0;
    for (int i = 0; key[i] != '\0'; i++)
    {
        hash += toupper(key[i]);
    }
    hash = hash % size;
    return hash;
}

int main(int argc, char* argv[])
{
    // get hash table size
    int size = get_int("Hash table size: ");

    // get key
    char* key = get_string("Key: ");

    // calculate and print index
    printf("The string '%s' is mapped to index %i\n", key,
    hash_function(key, size));

    return 0;
}