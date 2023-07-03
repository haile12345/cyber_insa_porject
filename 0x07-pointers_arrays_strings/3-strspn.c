#include "main.h"
/**
*_strspn - search the number of bytes in the initial
* segment of s which consist only of bytes from accept
*@s:segment targeted
*@accept:reference bytes container
*
*Return:returns the number of bytes in the initial
* segment of s which consist only of bytes from accept
*/
unsigned int _strspn(char *s, char *accept)
{
	unsigned int bytes = 0;
	int k;

	while (*s)
	{
		for (k = 0; accept[k]; k++)
		{
			if (accept[k] == *s)
			{
				bytes++;
				break;
			}
			else if ((accept[k + 1]) == '\0')
				return (bytes);
		}
		s++;
	}
	return (bytes);
}
