// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 150000

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

node *addNode(node *pointer, char *word);

// Represents a hash table
node *hashtable[N];

// global variable to keep track of words loaded
unsigned int counter = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char* word)
 {
     unsigned long hash = 5381;
     for (const char* ptr = word; *ptr != '\0'; ptr++)
     {
         hash = ((hash << 5) + hash) + tolower(*ptr);
     }
     return hash % N;
 }

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
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
    char buffer[LENGTH + 1];

    // Insert words into hash table
    int hashNum;
    while (fscanf(file, "%s", buffer) != EOF)
    {
        // hash buffer
        hashNum = hash(buffer);
        
        // add node to linked list
        hashtable[hashNum] = addNode(hashtable[hashNum], buffer);
        
        counter++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // int counter = 0;
    // node *list = NULL;
    
    // for (int i = 0; i < N; i++)
    // {
    //     // point to linked list in row i of hashtable
    //     list = hashtable[i];
        
    //     // count number of items in list
    //     while (list != NULL)
    //     {
    //         counter++;
    //         list = list -> next;
    //     }
    // }
    return counter;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int hashNum = hash(word);
    node *list = hashtable[hashNum];
    char tmp[LENGTH];
    strcpy(tmp, word);
    for (int i = 0; i < strlen(word); i++)
    {
        tmp[i] = tolower(word[i]);
    }
    while (list != NULL)
    {
        if (strcmp(list -> word, tmp) == 0)
        {
            // printf("%s", list->word);
            return true;
        }
        list = list -> next;
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 1; i < N; i++)
    {
        if (hashtable[i] != NULL)
        {
            node *tmp = hashtable[i] -> next;
            free(hashtable[i]);
            hashtable[i] = tmp;
        }
    }
    return true;
}

node *addNode(node *pointer, char *word)
{
    // create new node
    node *new_node = malloc(sizeof(node));
    // Check that enough memory is available
    if (new_node == NULL)
    {
        fprintf(stderr, "Not enought memory\n");
        return false;
    }
    new_node -> next = pointer;
    strcpy(new_node -> word, word);
    return new_node;
}
