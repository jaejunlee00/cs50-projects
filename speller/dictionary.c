// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

//boolean to be used for size
bool load_successful = false;

//counter for size
int counter = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
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
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        //'\0' needed to take care of substrings
        word[strlen(word)] = '\0';
        int n = hash(word);

        node *newnode = malloc(sizeof(node));
        if (newnode == NULL)
        {
            unload();
            return false;
        }
        // copy string and store pointer to the beginning of hashtable
        strcpy(newnode->word, word);
        newnode->next = hashtable[n];
        // link "head" to newly added node pointer
        hashtable[n] = newnode;
        counter++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    load_successful = true;
    return true;


}


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (load_successful)
    {
        return counter;
    }

    return 0;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    char wordcopy[LENGTH+1];
    // lowercase word and store in wordcopy
    for (int i = 0; i<LENGTH; i++)
    {
        wordcopy[i] = tolower(word[i]);
    }
    // need this to take care of substrings
    wordcopy[LENGTH] = '\0';


    int n = hash(wordcopy);
    // node cursor points at the beginning of hashtable
    node *cursor = hashtable[n];

    while (cursor != NULL)
    {

        if (strcasecmp(cursor->word, wordcopy) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }

    }



    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        // node cursor pointing at the beginning of hashtable
        node *cursor = hashtable[i];
        while (cursor !=NULL)
        {
            // temporary node to keep the linked lists
            node *temp =cursor;
            // traverse the cursor one time, then free the previous node pointer
            cursor = cursor->next;
            free(temp);
        }

    }
    load_successful = false;
    return true;
}
