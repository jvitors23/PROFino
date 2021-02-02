#include <stdint.h>
#include <stdio.h>

void send(char *func_name, uint32_t clock, uint8_t type) {
	printf("$%s@%llu@%d#\n", func_name, clock, type);
}
