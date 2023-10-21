#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    int key;
    string plaintext;

    // One command-line, only digits
    if (argc == 2 && only_digits(argv[1]))
    {
        key = atoi(argv[1]);
        plaintext = get_string("plaintext: ");
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    printf("ciphertext: ");

    // Rotating characters
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char c = plaintext[i];
        if (isalpha(c))
        {
            char rotated = rotate(c, key);
            printf("%c", rotated);
        }
        else
        {
            printf("%c", c);
        }
    }
    printf("\n");
    return (0);
}

bool only_digits(string s)
{
    int length = strlen(s);
    for (int i = 0; i < length; i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}

char rotate(char c, int k)
{
    if (isupper(c))
    {
        return 'A' + (c - 'A' + k) % 26;
    }
    else if (islower(c))
    {
        return 'a' + (c - 'a' + k) % 26;
    }
    return c;
}