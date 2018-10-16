#include <stdio.h>
#include <cs50.h>

int height;
int rows;
int space;
int hash;

int main(void)
{
    do
    {
    printf("Height: ");
    height = get_int();
    }   
while (height < 0 || height > 23);

    for (rows = 1; rows <= height; rows++)
    {
        for (space = 0; space < (height - rows); space++)
        {
        printf(" ");
        }
        
        for (hash = 1; hash <= rows; hash++)
        {
            printf("#");
        }
        
        printf("  ");
    
        for (hash = 1; hash <= rows; hash++)
        {
            printf("#");
        }
        
        printf("\n");
    }
}