#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // check if argc = 2, else return 1
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    
    // do some declaring here
    string k = argv[1];
    int l = strlen(argv[1]);
    
    // iterate over characters in key
    for (int i = 0, n = strlen(k); i < n; i++)
    {
        // check if k[i] is a letter 
        if (isalpha(k[i]))
        {
            // convert letters a-z in key to 0-25 regardless of case
            if (isupper(k[i]))
            {
                k[i] -= 65;
            }
            if (islower(k[i]))
            {
                k[i] -= 97;
            }
        }
        else
        {
            printf("Usage: ./caesar k\n");
            return 1;
        }
    }
    printf("plaintext:  ");
    string p = get_string();
    if (p != NULL)
    printf("ciphertext: ");
    {
        // iterate over characters in plaintext
        for (int i = 0, j = 0, m = strlen(p); i < m; i++)
        {
            
            // check if p[i] is a letter 
            if (isalpha(p[i]))
            {
                // key loops l ("L, length of key") times, then resets
                if (j == l)
                {
                    j = 0;
                }
                // make letter wrap around if necessary
                if ((p[i] <= 90 && p[i] + k[j] > 90) || (p[i] <= 122 && p[i] + k[j] > 122))
                {
                    p[i] -= 26;
                }
            // scramble
            printf("%c", p[i] + k[j]);
            j++;
            }
            // if not a letter, don't use key
            else
            printf("%c", p[i]);
            }
        printf("\n");
    }
    return 0;
}