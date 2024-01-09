#include "main.h"

/**
 *  print_last_digit - last digit
 *
 *@n: The int to print
 * Return: Always 0.
 */

int print_last_digit(int n)

{
int haile;

if (n < 0)
{
haile = (-1 * (n % 10));
_putchar (haile + '0');
return (haile);
}

else
{
haile = (n % 10);
_putchar (haile + '0');
return (haile);
}

}
