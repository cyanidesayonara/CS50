#include <stdio.h>
#include <cs50.h>

long long cc_number, i, j;
int x1, x2, checksum;

int main(void)
{
    do
    {
    printf("Number: ");
    cc_number = get_long_long();
    }
while (cc_number < 0);
    
for (i = cc_number; i > 0; i /= 100)
    x1 += i % 10;

for (j = cc_number / 10; j > 0; j /= 100)
{
    if ((j % 10) * 2 > 8)
    {
        x2 += ((j % 10) * 2) / 10;
        x2 += ((j % 10) * 2) % 10;
    }
    else
    x2 += (j % 10) * 2;
}

checksum = x1 + x2;

if (checksum % 10 == 0)
{
    if (cc_number > 5100000000000000 && cc_number < 5600000000000000)
    printf("MASTERCARD\n");
    else if ((cc_number >=4000000000000 && cc_number < 5000000000000) || (cc_number >=4000000000000000 && cc_number < 5000000000000000))
    printf("VISA\n");
    else if ((cc_number >= 340000000000000 && cc_number < 350000000000000) || (cc_number >= 370000000000000 && cc_number < 380000000000000))
    printf("AMEX\n");
    else
    printf("INVALID\n");
}
else
printf ("INVALID\n");

return 0;
}