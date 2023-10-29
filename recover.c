#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t byte;

int main(int argc, char *argv[])
{
    // Defining Errors
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *lost_file = fopen(argv[1], "r");
    if (lost_file == NULL)
    {
        printf("Can't open file\n");
        return 1;
    }

    FILE *current_file = NULL;
    char filename[8];
    int count = 0;

    byte buffer[512];
    while (fread(buffer, sizeof(byte), 512, lost_file))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (current_file != NULL)
            {
                fclose(current_file);
            }
            sprintf(filename, "%03i.jpg", count);
            current_file = fopen(filename, "w");
            count++;
        }
        if (current_file != NULL)
        {
            fwrite(buffer, sizeof(byte), 512, current_file);
        }
    }

    fclose(current_file);
    fclose(lost_file);
    return 0;
}
