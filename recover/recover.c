#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int COUNT = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Enter file to open.\n");
        return 1;
    }
     // open input file
    FILE* input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open card.raw\n");
        return 1;
    }
    bool jpgfound = false;
    int filecount = 0;
    int buffersize = COUNT;
    unsigned char buffer[COUNT];
    FILE *img = NULL;

    while (fread(buffer, buffersize, 1, input) == 1)
    {
        // when the "head" of jpeg is found, initially jpgfound is still false. jpgfound will be true AFTER
        // writing bytes to img file so that when the next "head" of jpeg is found I can close img.
        if (buffer[0]==0xff && buffer[1]==0xd8 && buffer[2]==0xff && (buffer[3]&0xf0) == 0xe0)
        {
            if (jpgfound == true)
            {
                fclose(img);
            }
            // print the .jpg name, open img, then set jpgfound = true.
            char filename[8];

            sprintf(filename, "%03i.jpg", filecount);
            filecount++;
            img = fopen(filename, "w");
            jpgfound = true;


        }

        if (jpgfound == true)
        {
            fwrite(&buffer, buffersize, 1, img);
        }
    }
    fclose(input);
    fclose(img);

}