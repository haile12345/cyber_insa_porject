#include "main.h"

/**
 * _islower - Short description, single line
 * @c: contains value to be compared
 * Return: Always 0.
 */
int _islower(int c)

{
for (char i = "a" ; i <= "z" ; i++)
{
if (c == i)
{
return (1);
}

else
{
continue;
}
}
return (0);
}
