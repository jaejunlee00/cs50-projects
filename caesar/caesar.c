#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
// check if there are two arguments
{
   
    if (argc == 2)
    {
        
        // iterate over the second argument, argv[1]
        for (int i=1; i<argc; i++)
        {
            // iterate over each element of second argument. This is to check if key is integer.
            for (int j=0, n = strlen(argv[1]); j<n; j++)
            {
                
            
                // if there's any alphabets, terminate the program
                if (isalpha(argv[1][j]))
                {
                    printf("Usage: ./caesar key\n");
                    return 1;
                }
                
            }
        // prompt the user here to terminate the program when argv is wrong
        // Done with checking argv[1] validity at this point.
            string plaintext = get_string("plaintext: ");
            string copytext = plaintext;
            
            
            for (int q = 0, m = strlen(plaintext); q<m; q++)
            {
                // convert ASCII to alph index
                if (isupper(plaintext[q]))
                {
                    copytext[q] = plaintext[q] - 65;
                    copytext[q] = (copytext[q]+atoi(argv[1])) % 26;
                    plaintext[q] = copytext[q] + 65;
                }
                else if (islower(plaintext[q])) 
                {

                    copytext[q] = plaintext[q] - 97;
                    copytext[q] = (copytext[q]+atoi(argv[1])) % 26;
                    plaintext[q] = copytext[q] + 97;
                }


            }

            
            printf("ciphertext: %s\n", plaintext);
            
           
        }
        
    }
    
    else
    {
        printf("Usage: ./caesar key\n");
    }
}


