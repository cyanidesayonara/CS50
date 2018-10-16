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
    
    printf("plaintext:  ");
    string p = get_string();
    // convert string argv[1] to int; if over 26, mod 26
    int k = atoi(argv[1]);
    if (k > 26)
    {
        k %= 26;
    }
    if (p != NULL)
    printf("ciphertext: ");
    {
        // iterate over characters in string
        for (int i = 0, n = strlen(p); i < n; i++)
            {
                // check if p[i] is a letter 
                if (isalpha(p[i]))
                {
                    // make letter wrap around if necessary
                    if ((p[i] <= 90 && p[i] + k > 90) || (p[i] <= 122 && p[i] + k > 122))
                    {
                        p[i] -= 26;
                    }
                printf("%c", p[i] + k);
                }
                // if not a letter, don't use key
                else
                printf("%c", p[i]);
            }
        printf("\n");
    }
    return 0;
}