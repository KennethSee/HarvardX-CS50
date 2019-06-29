#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int num = 0;
    while (num < 1 || num > 8)
    {
        num = get_int("What is your number?\n");
    }
    for (int i = 1; i <= num; i++)
    {
        for (int j = 1; j <= num + 2 + i; j++)
        {
            if (j <= num - i || j == num + 1 || j == num + 2)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}
