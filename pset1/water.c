#include <stdio.h>
#include <cs50.h>

int minutes;
int bottles;

int main(void)
{
    printf("Minutes: ");
    minutes = get_int();
    
    
    if (minutes > 0)
    {
        bottles = ((minutes * 1.5) * 128) / 16;
        printf("Bottles: %i\n", bottles);
    }
}

 