#include <stdio.h>
#include <avr/io.h>
#include <util/delay.h>
#include "comm/uart.h"

int main(void) { 
  uart_init();
  stdout = &uart_output;
  _delay_ms(5000);   

    while(1) {
      puts("Hello world!sdadasdasdasdasdsad");
      _delay_ms(1000);
     
    }
    
    return 0;
}