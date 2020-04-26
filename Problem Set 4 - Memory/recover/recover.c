// recovers JPEGs from a forensic image

#include <stdio.h>
#include <stdlib.h>

// defines a block of size 512
#define BLOCK 512

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover card.raw\n");
        return 1;
    }

    char *raw_file = argv[1];

    // open file
    FILE *inptr = fopen(raw_file, "r");

    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s\n", raw_file);
        return 2;
    }

    // output file pointer
    FILE *outptr = NULL;

    // counter for how many jpegs found
    int jpeg_counter = 0;

    // flag to check if jpegs have been found
    int jpeg_found = 0;

    // creating size of filenames for jpeg files
    char title[8];

    // create an unsigned character buffer, in which the memory will be stored
    unsigned char buffer[BLOCK];

    // while the file is able to read 1
    while (fread(buffer, BLOCK, 1, inptr) == 1)
    {
        // check first 4 bytes to check if jpeg is found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // check if jpeg has already been found and close it to start new jpeg file
            if (jpeg_found == 1)
            {
                // close the file to start a new one because a new jpeg has been found
                fclose(outptr);

            }
            else
            {
                // open first jpeg file and say that a jpeg has been found
                jpeg_found = 1;

            }

            // naming jpeg files
            sprintf(title, "%03d.jpg", jpeg_counter++);

            //open jpeg file
            outptr = fopen(title, "w");

        }

        // start writing the jpeg to the card
        if (jpeg_found == 1)
        {
            fwrite(&buffer, BLOCK, 1, outptr);
        }

    }
    // close files
    if (outptr != NULL)
    {
        fclose(outptr);
    }
    fclose(inptr);


    // success
    return 0;
}