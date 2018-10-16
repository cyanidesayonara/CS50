#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

// declare ints
int i, n;

int main(void)
{
    // get string, check if null
    string s = get_string();
    if (s != NULL)
    {
        // iterate over characters in string
        for (i = 0, n = strlen(s); i < n; i++)
        {
            // print character that matches conditions
            if ((s[i - 1] == '\0' && s[i] != ' ') || (s[i - 1] == ' ' && s[i] != ' '))
            printf("%c", toupper (s[i]));
        }
        printf("\n");
    }        
}