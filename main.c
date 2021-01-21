#include <util/delay.h>

float isPar(int num){

  _delay_ms(2000);

  if(num % 2 == 0){
    return 1;
  }else{
    return 0; 
  }

  return -1;}

int main(void) {
    while(1) {       
      int a = isPar(22);
      _delay_ms(1000);     
    }
    return 0;
}