#include "main.h"

/**
 * int_abs - return 0 letter not lowercase, 1 letter lowercase
 *
 *@n: the int to print
 * Return: Always 0.
 */
int int_abs(int n)
{
if (n > 0)
{
return (n);
}

else if (n == 0)
{
return (n);
}

else
{
n = n * -1;
return (n);
}

}
