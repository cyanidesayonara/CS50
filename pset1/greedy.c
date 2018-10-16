#include <stdio.h>
#include <cs50.h>

float change;
int cents, coins;

int main(void)
{
    do
    {
    printf("O hai! How much change is owed?\n");
    change = get_float();
    }
while (change < 0);

    cents = (change * 100);

while (cents >= 25)
    {
    coins ++;
    cents -= 25;
    }

while (cents >= 10)
    {
    coins ++;
    cents -= 10;
    }

while (cents >= 5)
    {
    coins ++;
    cents -= 5;
    }

    coins = cents + coins;
   
    printf("%i\n", coins);
}