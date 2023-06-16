#include <stdio.h>

/**
 * main - Entry point of the program
 *
 * Description: Prints the lowercase alphabets from 'a' to 'z'.
 *
 * Return: 0 if successful
 */
int main(void)
{
	char i;

	for (i = 97; i <= 122; i++)
	{
		putchar(i);
	}

	putchar('\n');

	return (0);
}

