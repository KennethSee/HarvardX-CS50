#include <stdio.h>
#include <stdlib.h>

int isJPEG_Check(unsigned char *buffer);

int main(int argc, char *argv[])
{
    // ensure only one command-line argument
    if (argc != 2)
    {
        fprintf(stderr, "./recover image\n");
        return 1;
    }
    
    // remember file name
    char *infile = argv[1];
    
    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    int jpg_number = 0;
    unsigned char *buffer = malloc(512);
    FILE *image;
    // execute while block has full 512 bytes
    while (fread(buffer, 1, 512, inptr) == 512)
    {
        int isJPEG = isJPEG_Check(buffer);
        if (isJPEG == 1)
        {
            // close previous image file
            if (jpg_number > 0)
            {
                fclose(image);
            }
            // create filename
            jpg_number++;
            char filename[7];
            sprintf(filename, "%03i.jpg", jpg_number - 1);
            // open new image file
            image = fopen(filename, "w");
        }
        
        // ignore if first JPEG is not yet found
        if (jpg_number > 0)
        {
            // write contents into new image file
            fwrite(buffer, 1, 512, image);
        }
    }
    
    // close infile and image
    fclose(image);
    fclose(inptr);
    
    free(buffer);
    
    // success
    return 0;
}

int isJPEG_Check(unsigned char *buffer)
{
    // printf("first val of buffer: %c\n", buffer[0]);
    // check if block is start of a JPEG file
    if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}
