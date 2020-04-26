#include <stdio.h>
#include <cs50.h>
#include <math.h>
 
int main (void)
{
   int fint;
   float f = 0;
   int coins = round(f * 10);
 
   float penny = 1;
   float nickel = 5;
   float dime = 10;
   float quarter = 25;
  
 
   do
   {
       f = get_float("Change owed: ");
       f = round(f * 100);
   }while (f < 0);
 
   while (f - quarter >= 0)
   {
       f = f - quarter;
       coins++;
   }
  
 
   while (f - dime >= 0)
   {
       f = f - dime;
       coins++;
   }
 
   while (f - nickel >= 0)
   {
       f = f - nickel;
       coins++;
   }
 
   while (f - penny >= 0)
   {
       f = f - penny;
       coins++;
   }
 
   //printf("%i\n", fint);
   printf("%i\n", coins);
 
  
 
 
 
}
 


