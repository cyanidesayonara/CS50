#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }
    
    // create pointers to in- and outfiles
    char* infile = argv[1];
    char* outfile = malloc(7 * sizeof(char)); //"kek.jpg"; 
    
    int a = 0;
    int i = 0;
    bool j = 0;
    bool k = 0;
    bool l = 0;
    
    //block size
    const n = 512;
    
    // buffer for read blocks
    char* buffer[n];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    do
    {
        // on first loop read first block into buffer
        if (l == 0)
        {
            fread(&buffer, n, 1, inptr);
        }
        
        // if at end of file, end loop
        if (feof(inptr))
        {
            //printf("\nEOF\n");
            j = 1;
        }
        
        // if first four bytes match jpg header
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] == 0xe0 || buffer[3] == 0xe1))
        {
            l = 1;
            
            // create filename in format ###.jpg
            sprintf(&outfile, "%03i.jpg", a);
            
            // open output file 
            FILE *outptr = fopen(outfile, "w");
            if (outptr == NULL)
            {
                fclose(outptr);
                fprintf(stderr, "Could not create %s.\n", outfile);
                return 3;
            }
            
            // start recovery by writing first block to file
            //printf("jpg header found in block %i (%i, %i, %i, %i)\n", i, buffer[0], buffer[1], buffer[2], buffer[3]);
            //printf("Recovering jpg (%03i)...\n", a);
            fwrite(&buffer, n, 1, outptr);
            k = 0;
            //sleep(1);

            do
            {
                // continue writing consecutive blocks...
                fread(buffer, n, 1, inptr);
                
                // ...until next header is found
                if (buffer[0] == 0xff &&
                buffer[1] == 0xd8 &&
                buffer[2] == 0xff &&
                (buffer[3] == 0xe0 || buffer[3] == 0xe1))
                {
                    // close file, return to start of original loop
                    //printf("Done!\n");
                    fclose(outptr);
                    k = 1;
                }
                
                // ...or until EOF is reached
                if (feof(inptr))
                {
                    fclose(outptr);
                    k = 1;
                }
                else {
                    fwrite(&buffer, n, 1, outptr);
                }
            } while (k == 0);
            a++;
        }
        i++;
    } while (j == 0);

    fclose(inptr);
    
    // free memory
    free(outfile);

    // success_kid.jpg
    return 0;
}