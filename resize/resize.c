// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    // remember filenames
    int scale = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // check scale
    if (scale <1 || scale >100)
    {
        printf("scale must be between 1 to 100\n");
        return 1;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    BITMAPFILEHEADER bfnew;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    bfnew = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    BITMAPINFOHEADER binew;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    binew = bi;

    binew.biWidth = bi.biWidth*scale;
    binew.biHeight = bi.biHeight*scale;



    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int newpadding = (4 - (binew.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    binew.biSizeImage = ((sizeof(RGBTRIPLE)*binew.biWidth)+newpadding)*abs(binew.biHeight);
    bfnew.bfSize = binew.biSizeImage+sizeof(BITMAPFILEHEADER)+sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bfnew, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&binew, sizeof(BITMAPINFOHEADER), 1, outptr);

    // determine padding for scanlines


    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        int rowcounter = 0;

        while (rowcounter<scale)
        {   // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;
                int pixelcounter = 0;
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                while (pixelcounter<scale)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                    pixelcounter++;
                }
            }

            for (int k = 0; k < newpadding; k++)
            {

                fputc(0x00, outptr);

            }

            if (rowcounter<(scale-1))
            {
                fseek(inptr, -(bi.biWidth*sizeof(RGBTRIPLE)), SEEK_CUR);
            }

            rowcounter++;
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);


    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
