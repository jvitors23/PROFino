.PHONY: all clean

# Files and dirs
SOURCE = main
SRC = $(SOURCE).c comm/uart.c 
OBJ = $(SRC:.c=.o)
EXTRAINCDIRS = comm

# Toolchain
CC = avr-gcc
NM = avr-nm
OBJCOPY = avr-objcopy
AVRDUDE = avrdude
REMOVE = rm -f

# GCC Flags
MCU = atmega328p
F_CPU = 16000000UL
COMPILE_CFLAGS = -Os -mmcu=$(MCU) -DF_CPU=$(F_CPU) 

# AVRDUDE Flags
MICROCONTROLLER = m328p
AVRDUDE_PROGRAMMER = arduino
BAUD_RATE = 115200

# Targets and recipes
all: elf hex

elf: $(SOURCE).elf
hex: $(SOURCE).hex
  
program: $(SOURCE).hex
	$(AVRDUDE) -c $(AVRDUDE_PROGRAMMER) -p $(MICROCONTROLLER) -P $(AVRDUDE_PORT) -b $(BAUD_RATE) -D -U flash:w:$(SOURCE).hex:i

%.hex: %.elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@

%.elf: $(OBJ)
	$(CC) -mmcu=$(MCU) $^ -o $@

%.o : %.c
	$(CC) $(COMPILE_CFLAGS) -c $< -o $@

clean: clean_list 
clean_list :
	$(REMOVE) $(SOURCE).hex
	$(REMOVE) $(SOURCE).elf
	$(REMOVE) $(OBJ)
