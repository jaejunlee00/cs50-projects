// h is hash, s is space

#include <cs50.h>
#include <stdio.h>

int get_positive_int(string prompt);

int main(void)
{
    int n = get_positive_int("Choose height: ");
    int x = n-1;
    
    for (int i = 0; i < n; i = i+1)
        
    {
        for (int s = 0; s < x ; s++)
        {
            printf(" ");
            
        }
        
        for (int h = 0; h<i+1; h++)
        {
            printf("#");
        }
       
        printf("\n");
        x = x-1;
      
    }
}

int get_positive_int(string prompt)
{
    int n;
    do
    {
        n = get_int("%s", prompt);
    }
    while (n < 1 || n > 8);
    return n;
}
