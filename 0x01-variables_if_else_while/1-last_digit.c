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
	int k = n % 10;

	if (k == 0)
		printf("Last digit of %d is %d and is 0\n", n, k);
	else if (k != 0 && k < 6)
		printf("Last digit of %d is %d and is less than 6 and not 0\n", n, k);
	else
		printf("Last digit of %d is %d and is greater than 6\n", n, k);

	return (0);
}

