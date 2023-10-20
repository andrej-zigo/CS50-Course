#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int row = 1; row <= height; row++)
    {
        for (int space = height - row; space > 0; space--)
        {
            printf(" ");
        }

        for (int block = 1; block <= row; block++)
        {
            printf("#");
        }
        printf("\n");
    }
}