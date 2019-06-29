#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int test_num_arg(int argc);
int validate_key(int argc, string argv[]);
int str_digits_convert(string s);;

int main(int argc, string argv[])
{
    int val1 = test_num_arg(argc);
    int val2 = validate_key(argc, argv);
    int c;
    if (val1 > 0 || val2 > 0)
    {
        return 1;
    }
    int key = str_digits_convert(argv[1]);
    printf("%i", key);
    string input = get_string("plaintext: \n");
    printf("\n");
    printf("ciphertext: ");
    for (int i = 0; i < strlen(input); i++)
    {
        if ((input[i] <= 90 && input[i] >= 65) || (input[i] >= 97 && input[i] <= 122))
        {
            if (islower(input[i]) > 0)
            {
                c = ((input[i] - 96 + key) % 26) + 96;
            }
            else
            {
                c = ((input[i] - 64 + key) % 26) + 64;
            }
            printf("%c", c);
        }
        else
        {
            printf("%c", input[i]);
        }
    }
    printf("\n");
    return 0;
}

int test_num_arg(int argc)
{
    if (argc != 2)
    {
//         printf("Usage: ./caesar key\n");
        return 1;
    }
//     printf("Success\n");
    return 0;
}

int validate_key(int argc, string argv[])
{
    int c;
    for (int i = 1; i < argc; i++)
    {
        for (int j = 0, n = strlen(argv[i]); j < n; j++)
        {
            c = argv[i][j];
            //printf("%i\n", c);
            if (c < 48 || c > 57)
            {
//                 printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }
//     printf("Success\n");
//     printf("%s\n", argv[1]);
    return 0;
}

int str_digits_convert(string s)
{
    int len = strlen(s);
    int num = 0;
    for (int i = 0; i < len; i++)
    {
        num += (s[i] - 48) * pow(10, len - 1 - i);
    }
    return num;
}
