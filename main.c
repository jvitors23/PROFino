#include <stdio.h>
#include <avr/io.h>
#include <util/delay.h>

#include "main.h"
#include "uart.h"

int main(void) {    

    uart_init();
    stdout = &uart_output;
    _delay_ms(2000);
    while(1) {
      puts("Hello world!");
      _delay_ms(1000);
    }
        
    return 0;
}