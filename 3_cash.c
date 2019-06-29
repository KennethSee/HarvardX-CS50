#include <cs50.h>
#include <stdio.h>
#include <math.h>

float min_coins(float x);

int main(void)
{
    float change_owed = -0.1;
    while (change_owed < 0)
    {
        change_owed = get_float("Change owed: \n");
    }
    int cents = round(change_owed * 100);
    int num = min_coins(cents);
    printf("%i \n", num);
}

float min_coins(float change_owed)
{
    float x = change_owed;
    int counter = 0;
    while (x > 0)
    {
        if (x - 25  >= 0)
        {
            x = x - 25;
            counter++;
        }
        else if (x - 10 >= 0)
        {
            x = x - 10;
            counter++;
        }
        else if (x - 5 >= 0)
        {
            x = x - 5;
            counter++;
        }
        else if (x - 1 >= 0)
        {
            x = x - 1;
            counter++;
        }
    }
    return(counter);
}
