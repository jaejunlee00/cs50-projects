#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
int shift(char c);

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
                
            
                // if there's any numbers, erminate the program
                if (isalpha(argv[1][j]) == false)
                {
                    printf("Usage: ./vigenere keyword\n");
                    return 1;
                }
                
                  
                    
            }
            string plaintext = get_string("plaintext: ");
            string copytext = plaintext;
                // prompt the user here to terminate the program when argv is wrong
                // Done with checking argv[1] validity at this point.
            int t = 0;
            for (int q = 0, m = strlen(plaintext); q<m; q++)
            {
                // convert ASCII to alpha index
                // apply the logic in walkthrough2
                // convert it back to ASCII
                              
                int p = strlen(argv[1]);
                int key = shift(argv[1][t%p]);
                
                if (isalpha(plaintext[q]))
                {
                    if (isupper(plaintext[q]))
                    {

                        copytext[q] = plaintext[q] - 65;
                        copytext[q] = (copytext[q]+key) % 26;
                        plaintext[q] = copytext[q] + 65;
                        
                    }
                    else if (islower(plaintext[q])) 
                    {

                        copytext[q] = plaintext[q] - 97;
                        copytext[q] = (copytext[q]+key) % 26;
                        plaintext[q] = copytext[q] + 97;
                                       
                    }
                    t++;                  
                }    
            }

   
            printf("ciphertext: %s\n", plaintext); 
        }  
    }
    
    else
    {
        printf("Usage: ./vigenere keyword\n");
    }
}

int shift(char s)
{
    if (islower(s))
        {
            s = toupper(s);
        }
        
    int c = (int) s;
    c = c - 65;
    return c;

}


