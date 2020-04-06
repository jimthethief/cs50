// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 3187

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Add item to start of linked list
void prepend(node **ptr, const char *str)
{
    // build new node
    node *new = malloc(sizeof(node));

    if (new == NULL)
    {
        exit(1);
    }

    // initialize new node
    strcpy(new->word, str);

    // add new node to head of list
    new->next = *ptr;
    *ptr = new;
}

// set counter to 0 for words in load function
int count = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
/*unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}
*/

// http://www.cse.yorku.ca/~oz/hash.html
unsigned long hash(const char *str)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *str++))
    {
        hash = ((hash << 5) + hash) + c;    /* hash * 33 + c */
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize all hash table buckets (ptrs) to NULL
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        char *new_word = word;
        int hashed = hash(new_word);
        prepend(&hashtable[hashed], new_word);
        count++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int n = strlen(word);
    char copy[strlen(word)];
    copy[n] = '\0'; // add null terminator to copy word

    // set copy word to lowercase
    for (int i = 0; i < n; i++)
    {
        copy[i] = tolower(word[i]);
    }

    // Get hash index for word
    int index = hash(copy);

    node *head = hashtable[index];

    for (node *ptr = head; ptr != NULL; ptr = ptr->next)
    {
        int i = strcasecmp(ptr->word, copy);
        // check each node
        if (i == 0)
        {
            // return true if we find value
            return true;
        }
    }
    // return false if we haven't found value
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // for each node in the hashtable
    for (int i = 0; i < N; i++)
    {
        // check the table for a node at that index
        node *ptr = hashtable[i];
        while (ptr != NULL)
        {
            // create a temporary node
            node *temp = ptr;
            ptr = ptr -> next;

            // free the current node
            free(temp);
        }
    }
    return true;
}