.PHONY: all clean

# Files and dirs
TARGET = main
SRC = $(TARGET).c comm/uart.c 
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
AVRDUDE_PORT = /dev/ttyACM0 # TODO: UTILIZAR ALTERNATIVA NÃO ESTÁTICA PARA RECONHECIMENTO DA PORTA

# Targets and recipes
all: elf sym hex

elf: $(TARGET).elf
sym: $(TARGET).sym
hex: $(TARGET).hex
  
program: $(TARGET).hex
	$(AVRDUDE) -c $(AVRDUDE_PROGRAMMER) -p $(MICROCONTROLLER) -P $(AVRDUDE_PORT) -b $(BAUD_RATE) -D -U flash:w:$(TARGET).hex:i

%.hex: %.elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@

%.sym: %.elf
	$(NM) -n $< > $@

%.elf: $(OBJ)
	$(CC) -mmcu=$(MCU) $^ -o $@

%.o : %.c
	$(CC) $(COMPILE_CFLAGS) -c $< -o $@

clean: clean_list 
clean_list :
	$(REMOVE) $(TARGET).hex
	$(REMOVE) $(TARGET).elf
	$(REMOVE) $(TARGET).sym
	$(REMOVE) $(OBJ)
