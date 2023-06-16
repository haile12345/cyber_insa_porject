#include <stdlib.h>
#include <time.h>
#include <stdio.h>

/**
 * main - Entry point of the program
 *
 * Description: Generates a random number and determines if it's positive,
 *              zero, or negative.
 *
 * Return: 0 if successful
 */
int main(void)
{
	int n;

	srand(time(0));
	n = rand() - RAND_MAX / 2;
	n = n % 10;

	if (n == 0)
		printf("is %d and is 0\n", n);
	else if (n > 0 || n < 6)
		printf("is %d and is less than 6 and not 0\n", n);
	else
		printf("is %d and is greater than 6\n", n);

	return (0);
}

