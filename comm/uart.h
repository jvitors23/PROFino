#include <stdio.h>
#include <stdint.h>

void uart_init();
uint8_t uart_getchar(FILE *stream);
void uart_putchar(uint8_t c, FILE *stream);

FILE uart_input = FDEV_SETUP_STREAM(NULL, uart_getchar, _FDEV_SETUP_READ);
FILE uart_output = FDEV_SETUP_STREAM(uart_putchar, NULL, _FDEV_SETUP_WRITE);
