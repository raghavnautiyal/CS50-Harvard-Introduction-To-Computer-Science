// Implements a dictionary's functionality
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 65355;

// Hash table
node *table[N];

// declare words to count the words in the dictionary
int dic_size = 0;

// Hashes word to a number, using the djb2 algorithm
unsigned int hash(const char *word)
{
    // set an integer named hash
    unsigned int hash = 0;

    // iterate through the dictionary
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash = (hash << 2) ^ word[i];
    }

    return hash % N;
}


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int len = strlen(word);

    char lword[len + 1];

    for (int i = 0; i < len; i++)
    {
        lword[i] = tolower(word[i]);
    }

    lword[len] = '\0';

    // hash the word and store it in a variable called hash_code
    int hash_code = hash(lword);

    // set a temporary variable, to store the linked list
    node *temp = table[hash_code];

    while (temp != NULL)
    {
        // check if the word in the dictionary matches with the word in the hash table
        if (strcasecmp(temp -> word, lword) != 0)
        {
            temp = temp -> next;
        }
        else
        {

            return true;
        }

    }

    return false;

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{

    // open up dictionary file
    FILE *dictionary_file = fopen(dictionary, "r");

    char *dictword = malloc(LENGTH + 1);

    // check to see if file is null
    if (dictword == NULL)
    {
        // if so, exit the loop
        return false;
    }

    // read strings from file one at a time
    while (fscanf(dictionary_file, "%s", dictword) != EOF)
    {

        // create a new node for each word using malloc
        node *n = malloc(sizeof(node));
        n -> next = NULL;

        // check if malloc is null
        if (n == NULL)
        {
            return false;
        }

        // copy each word into a node using strcpy
        strcpy(n -> word, dictword);

        // increment size variable
        dic_size++;

        // set next to point at beginning of list
        n -> next = table[hash(dictword)];

        // set array to point at n which becomes new beginning of the list
        table[hash(dictword)] = n;


    }
    fclose(dictionary_file);
    free(dictword);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{

    return dic_size;

}

// destroys all nodes. RECURSIVE FUNCTION!
void destroy(node *head)
{
    if (head -> next != NULL)
    {
        destroy(head -> next);
    }
    free(head);
}


// frees all memory
bool unload(void)
{
    for (int i = 0; i < N - 1; i++)
    {
        if (table[i] != NULL)
        {
            destroy(table[i]);
        }
    }
    return true;
}
