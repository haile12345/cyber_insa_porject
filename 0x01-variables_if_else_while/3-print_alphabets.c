/*
 * File: 3-print_alphabets.c
 * Auth: Solomon Kassa
 */

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
		putchar(letter);

	for (letter = 65 ; letter <= 90; letter++)
		putchar(letter);

	putchar('\n');

	return (0);
}

