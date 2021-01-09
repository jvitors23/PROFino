# FLAGS
MCU = atmega328p
MICROCONTROLLER = m328p
F_CPU = 16000000
TARGET = main
SRC = $(TARGET).c comm/uart.c
OBJ = $(SRC:.c=.o)
EXTRAINCDIRS = comm
AVRDUDE_PROGRAMMER = arduino
BAUD_RATE = 115200
AVRDUDE_PORT = /dev/ttyACM0
CC = avr-gcc
OBJCOPY = avr-objcopy
AVRDUDE = avrdude
REMOVE = rm -f
COMPILE_CFLAGS = -Os -mmcu=$(MCU) -DF_CPU=$(F_CPU)UL  

# Default target.
all: elf hex

elf: $(TARGET).elf
hex: $(TARGET).hex
  
program: $(TARGET).hex
	$(AVRDUDE) -c $(AVRDUDE_PROGRAMMER) -p $(MICROCONTROLLER) -P $(AVRDUDE_PORT) -b $(BAUD_RATE) -D -U flash:w:$(TARGET).hex:i

%.hex: %.elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@

%.elf: $(OBJ)
	$(CC) -mmcu=$(MCU) $^ -o $@

%.o : %.c
	$(CC) -c $(COMPILE_CFLAGS) $< -o $@ 

clean: clean_list 

clean_list :
	$(REMOVE) $(TARGET).hex
	$(REMOVE) $(TARGET).elf
	$(REMOVE) $(OBJ)