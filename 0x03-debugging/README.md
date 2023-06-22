0x03. C - Debugging
GENERAL 📖📖📖:
What is debugging
What are some methods of debugging manually
How to read the error messages
RESOURCES:
Debugging
Rubber Duck Debugging
INTRODUCTION TO FILES 📕📕📕:
0-main.c: In most projects, we often give you only one main file to test with. For example, this main file is a test for a postitive_or_negative() function similar to the one you worked with in an earlier C projectBased on the main.c file above, create a file named 0-main.c. This file must test that the function positive_or_negative() gives the correct output when given a case of 0.You are not coding the solution / function, you’re just testing it! However, you can adapt your function from 0x01. C - Variables, if, else, while - Task #0 to compile with this main file to test locally.
1-main.c: Copy this main file. Comment out (don’t delete it!) the part of the code that is causing the output to go into an infinite loop.Your output should look like this
2-largest_number.c: This program prints the largest of three integers.? That’s definitely not right.Fix the code in 2-largest_number.c so that it correctly prints out the largest of three numbers, no matter the case.
3-print_remaining_days.c: This program converts a date to the day of year and determines how many days are left in the year, taking leap year into consideration.Output looks good for 04/01/1997! Let’s make a new main file 3-main_b.c to try a case that is a leap year 02/29/2000.? That doesn’t seem right.Fix the print_remaining_days() function so that the output works correctly for all dates and all leap years.
FILES 📑📑📑:
0-main.c

In most projects, we often give you only one main file to test with. For example, this main file is a test for a postitive_or_negative() function similar to the one you worked with in an earlier C project

Based on the main.c file above, create a file named 0-main.c. This file must test that the function positive_or_negative() gives the correct output when given a case of 0.

You are not coding the solution / function, you’re just testing it! However, you can adapt your function from 0x01. C - Variables, if, else, while - Task #0 to compile with this main file to test locally.

carrie@ubuntu:/debugging$ cat main.c
#include "holberton.h"

/**
* main - tests function that prints if integer is positive or negative
* Return: 0
*/

int main(void)
{
        int i;

        i = 98;
        positive_or_negative(i);

        return (0);
}
carrie@ubuntu:/debugging$
1-main.c

Copy this main file. Comment out (don’t delete it!) the part of the code that is causing the output to go into an infinite loop.

Your output should look like this

carrie@ubuntu:/debugging$ cat 1-main.c
#include <stdio.h>

/**
* main - causes an infinite loop
* Return: 0
*/

int main(void)
{
        int i;

        printf("Infinite loop incoming :(\n");

        i = 0;

        while (i < 10)
        {
                putchar(i);
        }

        printf("Infinite loop avoided! \\o/\n");

        return (0);
}
carrie@ubuntu:/debugging$
2-largest_number.c

This program prints the largest of three integers.

? That’s definitely not right.

Fix the code in 2-largest_number.c so that it correctly prints out the largest of three numbers, no matter the case.

carrie@ubuntu:/debugging$ cat 2-main.c
#include <stdio.h>
#include "holberton.h"

/**
* main - prints the largest of 3 integers
* Return: 0
*/

int main(void)
{
        int a, b, c;
        int largest;

        a = 972;
        b = -98;
        c = 0;

        largest = largest_number(a, b, c);

        printf("%d is the largest number\n", largest);

        return (0);
}
carrie@ubuntu:/debugging$
3-print_remaining_days.c

This program converts a date to the day of year and determines how many days are left in the year, taking leap year into consideration.

Output looks good for 04/01/1997! Let’s make a new main file 3-main_b.c to try a case that is a leap year 02/29/2000.

? That doesn’t seem right.

Fix the print_remaining_days() function so that the output works correctly for all dates and all leap years.

carrie@ubuntu:/debugging$ cat 3-main_a.c
#include <stdio.h>
#include "holberton.h"

/**
* main - takes a date and prints how many days are left in the year, taking
* leap years into account
* Return: 0
*/

int main(void)
{
    int month;
    int day;
    int year;

    month = 4;
    day = 01;
    year = 1997;

    printf("Date: %02d/%02d/%04d\n", month, day, year);

    day = convert_day(month, day);

    print_remaining_days(month, day, year);

    return (0);
}

