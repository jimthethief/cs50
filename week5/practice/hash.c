
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>

// Represents number of buckets in a hash table
#define N 26
#define LENGTH 45

// Represents a node in a hash table
typedef struct sllist // temporary name to use in line 17 - need way to refer to data type
{
    int val; // data stored in node
    struct sllist *next; // pointer to next node
}
sllnode; // defines name of node

sllnode* head = NULL; // set start value of head pointer to NULL

void create(int i);
bool find(sllnode* list, int j);
void insert(sllnode* list, int k);
void destroy(sllnode** list);
unsigned int hash(char* str);
int hash2(char* key);

int main(void)
{
    // 1. Create a link list from scratch
        // pseudo: sllnode* create(VALUE[e.g. int] val); - should create pointer to singly-linked node
        // see create function
    create(6);
    printf("Head is pointing to: %i\n", head->val);
    // 2. Search through linked list to find element
        // see find function
    find(head, 24);
    // 3. Insert a new node into the linked list
    insert(head, 24);
    find(head, 24);
    int num = get_int("Enter a number: ");
    insert(head, num);
    find(head, num);
    printf("Head is pointing to %i.\n", head->val);
    printf("The full list is: \n");
    for (sllnode* ptr = head; ptr != NULL; ptr = ptr->next)
    {
        printf("%i\n", ptr->val);
    }
    // 4. Delete a single element from a linked list
        // Only plausible in doubly linked lists
    // 5. Delete an entire list - free memory
        // see destroy function
    destroy(&head);
    printf("The full list is: \n");
    sllnode* point = head;
    if (point != NULL)
    {
        for (sllnode* ptr = head; ptr != NULL; ptr = ptr->next)
        {
            printf("%i\n", ptr->val);
        }
    }
    else printf("...Empty!\n");
    char* word = "Calculator";
    hash(word);
    hash("gigantic");
    hash("calculus");
    hash2(word);

}

void create(int i)
{
    // a. Dynamically allocate space for new sllnode
    sllnode* new_node = malloc(sizeof(sllnode));

    // b. Check to make sure we didn't run out of memory
    if (new_node == NULL) // Check that malloc returns enough memory
    {
        printf("Sorry, something's not right: Memory error");
    }

    // c. Initialise the node's val field - data stored in node
    new_node->val = i;

    // d. Initialise the node's next field - pointer to next node
    new_node->next = NULL; // Not pointing to anything so NULL

    // e. Set head pointer to the newly created sllnode
    head = new_node;
}

bool find(sllnode* list, int j)
{
    // a. create traversal pointer to the list's head - duplicate ptr prevents unchaining list
    for (sllnode* ptr = list; ptr != NULL; ptr = ptr->next)
    {
        // b. if current node's val matches searched for val - report success
        if (ptr->val == j)
        {
            printf("Yay! I found %i in the list.\n", j);
            return true;
        }
    }
    // c. if not, set traversal ptr to next ptr & repeat step b
    // d. if end of list is reached without success - report failure
    printf("Sorry, I can't find %i in the list.\n", j);
    return false;
}

void insert(sllnode* list, int k)
{
    // a. Dynamically allocate space for new sllnode
    sllnode* new_node = malloc(sizeof(sllnode));

    // b. Check to make sure we didn't run out of memory
    if (new_node == NULL) // Check that malloc returns enough memory
    {
        printf("Sorry, something's not right: Memory error");
    }

    // c. Initialise the node's val field - data stored in node
    new_node->val = k;

    // d. Initialise the node's next field - pointer to next node
    new_node->next = NULL; // Not pointing to anything so NULL

    // e. Set head pointer to the newly created sllnode without breaking chain
    new_node->next = list;
    head = new_node;
}

// Function to delete entire linked list
void destroy(sllnode** list)
{
    sllnode* cur = *list; // deref list to get the real head
    sllnode* nxt;

    while (cur != NULL) // a. If you've reached a NULL ptr, stop
    {
        // b. Otherwise, delete *the rest of the list*
        nxt = cur->next;
        free(cur); // c. Free the current node
        cur = nxt;
    }
    *list = NULL; // deref list to affect the real head back

}

// Hash table consists of two things:
    // 1.  a hash function: returns a non-negative integer value HASH CODE
    // a good hash function:
        // - only uses the data being hashed
        // - uses all of the data being hashed
        // - is deterministic:
            // every time same data passed in, same hash code comes out
        // - uniformly distributes the data
        // - generate v. different hash codes for v. different data

    // 2. an array: capable of storing data of the same type we want to...
    // ... place in the data structure

// SIMPLE (but not particularly great) CS50 EXAMPLE
unsigned int hash(char* str)
{
    int hash = 0; // initialise hash & set to 0
    for (int j = 0; str[j] != '\0'; j++) // detect end of string (like strlen)
    {
        hash += str[j]; // add ascii value of current char to value of hash
    }

    hash = hash % N;
    printf("%u\n", hash);
    return hash;
}

// ANOTHER CS50 EXAMPLE
// first letter of a string determines hash table index for that string
// e.g. words starting with 'a' are assigned to index 0, 'b' to index 1...

int hash2(char* key)
{
    // hash the first letter of string
    int hash = toupper(key[0] - 'A');
    hash = hash % N;
    printf("%i\n", hash);
    return hash;
}

// Collisions occur if two pieces of data yield the same hash code

    // LINEAR PROBING is one way to get both elements into the hash table
    // while preserving quick insertion and lookup
    // This method prevents collisions by placing data in the next
    // consecutive element until vacancy is found hashcode + 1, hashcode + 2...
    // Can lead to problem called CLUSTERING - once there's a miss,
    // two adjacent cells contain data, leading to higher likelihood of
    // cluster growing
    // Also, can only store as much data as locations in array (N 26 here)

    // CHAINING uses linked lists to solve this problem:
    // Each element of the array is a pointer to the head of a linked list
        // multiple pieces of data can yield same hash code and still be
        // safely stored! WUNDERBAR.


// So instead of string hashtable[N]; - hashtable is now node* hashtable[N];
    // from a hashtable capable of storing N strings...
    // to a hashtable capable of storing N pointers to heads of linked lists

// so, if hash("Joey"); returns hashcode 6
// we need to dynamically allocate space for Joey
// THEN add him to the chain at location 6

