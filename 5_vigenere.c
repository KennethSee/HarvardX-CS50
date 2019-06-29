#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int test_num_arg(int argc);
int validate_key(int argc, string argv[]);
int shift(char c);

int main(int argc, string argv[])
{
    int val1 = test_num_arg(argc);
    int val2 = validate_key(argc, argv);
    int c;
    if (val1 > 0 || val2 > 0)
    {
        return 1;
    }

    int key;
    int keyLength = strlen(argv[1]);
    int keyPos = 0;

    string input = get_string("plaintext: \n");

    printf("ciphertext: ");
    for (int i = 0; i < strlen(input); i++)
    {
        if ((input[i] <= 90 && input[i] >= 65) || (input[i] >= 97 && input[i] <= 122))
        {
            if (keyPos == keyLength)
            {
                keyPos -= keyLength;
            }
            key = shift(argv[1][keyPos]);
            if (islower(input[i]) > 0)
            {
                c = ((input[i] - 96 + key) % 26) + 96;
            }
            else
            {
                c = ((input[i] - 64 + key) % 26) + 64;
            }
            keyPos++;
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
//         printf("Usage: ./vigenere key\n");
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
            if (c < 65|| c > 122 || (c > 90 && c < 97))
            {
//                 printf("Usage: ./vigenere key\n");
                return 1;
            }
        }
    }
//     printf("Success\n");
//     printf("%s\n", argv[1]);
    return 0;
}

int shift(char c)
{
    if (c < 97)
    {
        c = c - 65;
    }
    else
    {
        c = c - 97;
    }
    return c;
}
