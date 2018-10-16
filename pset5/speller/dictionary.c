/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <unistd.h>

#include "dictionary.h"

#define HASHTABLE 65536

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

int words = 0;

node *hashtable[HASHTABLE] = {NULL};

unsigned int hash(const char *word);

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    //hash for word
    int hashed = hash(word);

    //pointer to first node in list
    node *trav = hashtable[hashed];
    
    // conpare word to nodes until match found or at end of list
    while (trav != NULL)
    {
        if (strcasecmp(trav->word, word) == 0)
        {
            return true;
        }
    trav = trav->next;
    }
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // file pointer for dictionary
    FILE *fp = fopen(dictionary, "r");

    if (fp == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return 1;
    }

    // char array for word
    char word[LENGTH+1];
    
    // scan a word from dict
    while (fscanf(fp, "%s", word) != EOF)
    {
        // create a hash for said word
        int hashed = hash(word);

        // ... create a pointer to a new node
        node *new = malloc(sizeof(node));

        if (new == NULL)
        {
            fclose(fp);
            unload();
            return false;
        }
        
        // copy word to node
        strcpy(new->word, word);
        
        // if position on hashtable is empty (points to NULL), node points to NULL and hashtable points to new node
        if (hashtable[hashed] == NULL)
        {
            new->next = NULL;
            hashtable[hashed] = new;
        }
        // else new node is added as head of linked list
        else
        {
            new->next = hashtable[hashed];
            hashtable[hashed] = new;
        }
        // increment word count
        words++;
    }
    // free file pointer
    fclose(fp);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // simply returns word count
    return words;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // iterate thru every pos on hashtable
    for (int i = 0; i < HASHTABLE; i++)
    {
        // pointer to first node on linked list
        node *trav = hashtable[i];

        // free nodes on linked list until trav points to NULL
        while (trav != NULL)
        {
            node *temp = trav;
            trav = trav->next;
            free(temp);
        }
    }
    
    return true;
}

unsigned int hash(const char *word)
{
    // hash algorithm from https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c
    unsigned long hash = 5381;

    for (const char* ptr = word; *ptr != '\0'; ptr++)
    {
        hash = ((hash << 5) + hash) + tolower(*ptr);
    }
    /**
    ** basic hash function using sum of letters
    int hash = 0;
    
    for (int i = 0; i < strlen(word); i++)
    {
        hash += word[i];
    }
    */
    return hash % HASHTABLE;
}