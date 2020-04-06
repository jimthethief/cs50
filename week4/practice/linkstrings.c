#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define SIZE 10
#define N 26

typedef struct node
{
    // the value to store in this node
    char s[SIZE + 1];

    // the link to the next node in the list
    struct node* next;
}
node;

node* hashtable[N];
void prepend(node** ptr, const char *str);


unsigned int hash(const char *word)
{
    return tolower(word[0] - 'a');
    /*int hash = tolower(word[0] - 'a');
    hash = hash % N;
    printf("%i\n", hash);
    return hash;
    */
}

bool check(const char *word);
bool unload(void);

int main(int argc, char* argv[])
{

    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }
    node* head;

    char* noun = "chair";
    char* cnoun = "Chair";

    int hashed = hash(noun);
    prepend(&hashtable[hashed], noun);
    // ONCE HASH FUNCTION IS MADE, HASH THE WORD
        // - node1->word has the word from the dictionary
        // - hashing node1->word will give us the index of a bucket in has table
        //  - insert into the linked list
    // insert words into hashtable:
    printf("%s\n", hashtable[hashed]->s);
    check(noun);
    check(cnoun);

    if (strcasecmp(noun, cnoun) == 0)
    {
        printf("%s is equal to %s in a case-insensitive string comparison", noun, cnoun);
    }
    check("arms");

    // printing out list
    printf("Your full list contains: \n");
    for (node*  ptr = hashtable[hashed]; ptr != NULL; ptr = ptr->next)
    {
        printf("- %s\n", ptr->s);
    }
    unload();
    printf("Your full list contains: \n");
    for (node*  ptr = hashtable[hashed]; ptr != NULL; ptr = ptr->next)
    {
        printf("- %s\n", ptr->s);
    }

    return 0;
}

bool check(const char *word)
{
    int n = strlen(word);
    char copy[n + 1];

    //Add null terminator to end of the lower case word
    copy[n] = '\0';

    for(int i = 0; i < n; i++)
    {
        copy[i] = tolower(word[i]);
    }

    // Get hash index for word
    int index = hash(copy);

    node* head = hashtable[index];

    for (node*  ptr = head; ptr != NULL; ptr = ptr->next)
    {
        int i = strcasecmp(ptr->s, copy);
        // check each node
        if (i == 0)
        {
            printf("Found %s.\n", word);
            // return true if we find value
            return true;
        }
    }
    // return false if we haven't found value
    printf("Couldn't find %s.\n", word);
    return false;
}

void prepend(node** ptr, const char *str)
{
    // build new node
    node* new = malloc(sizeof(node));

    if (new == NULL)
    {
        exit(1);
    }

    // initialize new node
    strcpy(new->s, str);

    // add new node to head of list
    new->next = *ptr;
    *ptr = new;
}

bool unload(void)
{
    // for each node in the hashtable
    for (int i = 0; i < N; i++)
    {
        // check the table for a node at that index
        node* ptr = hashtable[i];
        while (ptr != NULL)
        {
            // create a temporary node
            node* temp = ptr;
            ptr = ptr -> next;

            // free the current node
            free(temp);
        }
    }
    return true;
}