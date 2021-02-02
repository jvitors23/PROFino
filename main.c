#include <util/delay.h>

void teste(){

  int a; 
  for (int i = 0; i < 10000; i++)  {
   int b  = i*i*i*i*i*i*i*i;
    for (int j = 0; j < 10000; j++)  {
      int c  = i*i*i*i*i*i*i*i;
      for (int k = 0; k < 10000; k++)  {
        int d  = i*i*i*i*i*i*i*i;
      }
    }
  }
  
}

int main(void){ 

  while(1) {    
    teste();
  }
  return 0;
}