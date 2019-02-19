#include <cs50.h>
#include <stdio.h>
#include <math.h>

float get_positive_float(string prompt);

int main(void)
{
    float f = get_positive_float("How much change? ");
    
    printf("Change owed: %.2f\n", f);
    int coins = round(f*100);
    
    int counter = 0;
    float q = 25;
    float d = 10;
    float n = 5;
    float p = 1;
    
    
    for (int i=0; coins>0; i++)
    {
        if (coins>=q)
        {
            coins = coins - q;
           
        }
        else if (coins>=d)
        {
            coins = coins - d;
           
        }
        else if (coins>=n)
        {
            coins = coins-n;
            
        }
        else if (coins>=p)
        {
            coins = coins-p;
        }
       
        counter++;
    
    }
    
  
    printf("%i\n", counter);
    
    
}
    
    
float get_positive_float(string prompt)
{
    float n;
    do
    {
        n = get_float("%s", prompt);
    }
    while (n < 0);
    return n;
}
