#include <stdio.h>
#include "comm/uart.h"
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// global variable to count the number of overflows
volatile int timer_overflow_count;
volatile int timer_overflow_count_overflow;
  
// initialize timer, interrupt and variable
void timer0_init(){
    // set up timer with prescaler = 256
    TCCR0B |= (1 << CS02);
  
    // initialize counter
    TCNT0 = 0;
  
    // enable overflow interrupt
    TIMSK0 |= (1 << TOIE0);
  
    // enable global interrupts
    sei();
  
    // initialize overflow counter variable
    timer_overflow_count = 0;
    timer_overflow_count_overflow = 0;
}
  
// TIMER0 overflow interrupt service routine
// called whenever TCNT0 overflows
ISR(TIMER0_OVF_vect){
    // keep a track of number of overflows
    timer_overflow_count++;
    if (timer_overflow_count >= 65000)  // NOTE: '>=' is used
    {  
      timer_overflow_count_overflow++; 
      TCNT0 = 0;            // reset counter
      timer_overflow_count = 0;     // reset overflow counter
    }
}

int main(void){
  uart_init();
  stdout = &uart_output;
  
  _delay_ms(2000);
  puts("inicio");
  puts("inicio");
  puts("inicio");
   // initialize timer
  // timer0_init();

  while(1) {    
    printf("joseojsejosjejosejosjeoseosjeojseojsoejsoejosjeo\n");

    // printf("overflow:%d:count_overflow:%d\n", timer_overflow_count, timer_overflow_count_overflow);
  }
  return 0;
}