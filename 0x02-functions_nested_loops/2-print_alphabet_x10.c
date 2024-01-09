#include "main.h"

/**
 * print_alphabet_x10 - print alphabet
 *
 * Return: Always 0.
 */
void print_alphabet_x10(void)
{
int i;
int count;


count = 0;
while (count < 10)
{
for (i = 97 ; i <= 122 ; i++)
{
_putchar(i);
}

count++;
_putchar('\n');
}


}
