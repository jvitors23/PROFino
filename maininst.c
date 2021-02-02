#include <util/delay.h>
#include <stdio.h>
#include "comm/uart.h"
#include "comm/send.h"
#include <avr/io.h>
#include <avr/interrupt.h>

volatile uint16_t timer_overflow_count;
volatile uint16_t timer_overflow_count_overflow;

void timer0_init(){
	TCCR0B |= (1 << CS02);
	TCNT0 = 0;
	TIMSK0 |= (1 << TOIE0);
	sei();
	timer_overflow_count = 0;
	timer_overflow_count_overflow = 0;
}

ISR(TIMER0_OVF_vect){
	timer_overflow_count++;
	if (timer_overflow_count >= 32000){
		timer_overflow_count_overflow++;
		timer_overflow_count = 0;
	}
}
void teste(){
printf("========:%d:%d:%s:%d:========\n", timer_overflow_count, timer_overflow_count_overflow, __func__, 1);
  for (int i = 0; i < 1000; i++)  {
    for (int j = 0; j < 1000; j++)  {
      for (int k = 0; k < 1000; k++)  {
        int a;
      }
    }
  }  
printf("========:%d:%d:%s:%d:========\n", timer_overflow_count, timer_overflow_count_overflow, __func__, 0);
}

// int main(void){ 

//   for (int i = 0; i < 10; i++) {
//     teste();
//   }

//   return 0;
// }


int main(void){ 
uart_init();
stdout = &uart_output;
_delay_ms(3000);
puts("=======:inicio:=======");
puts("=======:inicio:=======");
puts("=======:inicio:=======");
timer0_init();

printf("========:%d:%d:%s:%d:========\n", timer_overflow_count, timer_overflow_count_overflow, __func__, 1);

  while(1) {
    teste();
  }
  
printf("========:%d:%d:%s:%d:========\n", timer_overflow_count, timer_overflow_count_overflow, __func__, 0);
  return 0;
printf("========:%d:%d:%s:%d:========\n", timer_overflow_count, timer_overflow_count_overflow, __func__, 0);
}