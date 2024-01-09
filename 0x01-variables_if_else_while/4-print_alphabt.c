#include <stdio.h>

/**
 * main - Prints the alphabet in lowercase, and then in uppercase.
 *
 * Return: Always 0.
 */
int main(void)
{
	char letter;

	for (letter = 97 ; letter <= 122; letter++)
		if (letter != 113 && letter != 101)
			putchar(letter);


	putchar('\n');

	return (0);
}
