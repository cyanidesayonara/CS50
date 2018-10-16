#define _XOPEN_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[])
{
    // check if argc = 2, else return 1
    if (argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }
    
    char salt[2];
    strncpy(salt, argv[1], 2);
    
    //create an array of possible characters
    char chars[] = {"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#"};
    int length = strlen(chars);
    
    // set everything to zero
    char word[5] = {0, '\0', '\0', '\0', '\0'};
    
    int j = 0;
    int k = 0;
    int l = 0;
    int counter = 0;
    
    // here we generate all possible combinations with used characters, using up to four characters
    // iterate over characters on array
    for (int i = 0; i < length; i++)
    {
        word[0] = chars[i];
        counter++;
       
        // if first character reaches end (0), go back to "a" and start iterating over next character
        if (word[0] == '#')
        {
            i = 0;
            word[1] = chars[j];
            word[0] = chars[0];
            j++;
            
            // add a new character...
            if (word[1] == '#')
            {
                i = 0;
                j = 0;
                word[2] = chars[k];
                word[0] = chars[0];
                word[1] = chars[0];
                k++;
                
                // ...and so on 
                if (word[2] == '#')
                {
                    i = 0;
                    j = 0;
                    k = 0;
                    word[3] = chars[l];
                    word[0] = chars[0];
                    word[1] = chars[0];
                    word[2] = chars[0];
                    l++;
                    
                    // ...until all possible combinations for four characters have been tried
                    if (word[3] == '#')
                    {
                        printf("All possible combinations exhausted, password can't be a-Z with up to four characters (current: %s)\n", word);
                        return 1;
                    }
                }
            }
        }
        
        /*
        if (counter % 1000 == 1)
        {
            printf("Cracking...");
        }
        if (counter % 1000 == 0)
        {
        printf("%i combinations tried (current: %s)\n", counter, word);
        }
        if (counter % 100000 == 0)
        {
            printf("Crack is wack!\n");
        }
        */
        
        // create a hash from word + salt using crypt and compare it against argv[1]
        if (strcmp(crypt(word, salt), argv[1]) == 0)
        {
            // print password
            //printf("\nPassword found in %i tries: ", counter);
            printf("%s\n", word);
            return 0;
        }
    }
}