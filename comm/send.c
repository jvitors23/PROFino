#include <stdio.h>
#include "uart.h"
#include <avr/io.h>

void send(char* address, int clock, char type){
  int checksum = 0;
  // Add calculo do checksum
  printf("$%s@%d@%c#%d\n", address, clock, type, checksum);
  
}

