# vim: ts=4 noet sw=4 sts=4 ai

CROSS_COMPILE ?= arm-none-eabi-

CC      := $(CROSS_COMPILE)gcc
OBJCOPY := $(CROSS_COMPILE)objcopy
OBJDUMP := $(CROSS_COMPILE)objdump
SIZE    := $(CROSS_COMPILE)size

PROJECT_NAME := $(shell basename `readlink -f .`)
TARGET       := $(PROJECT_NAME).bin

CFILES := $(wildcard src/*.c)
OFILES := $(CFILES:src/%.c=build/%.o)

ifeq ($(DEBUG),1)
	CFLAGS := -O0
else
	CFLAGS := -Os
endif

CFLAGS  += -g3 -Wall -mtune=cortex-a8 -std=gnu99 -ffreestanding -nostdinc
LDFLAGS := -nostartfiles -nodefaultlibs -nostdlib -static
INCLUDE := -I./include -I./src
 
.SECONDARY:
.PHONY: all
all: build/$(PROJECT_NAME).bin build/$(PROJECT_NAME).dis

-include $(wildcard build/*.d)

$(shell mkdir -p build)

build/%.o: src/%.c
	$(CC) -c $(CFLAGS) $(INCLUDE) -MMD -MP -MF build/$*.d $< -o $@

build/%.elf: src/$(PROJECT_NAME).ld $(OFILES)
	$(CC) $(CFLAGS) $(LDFLAGS) -Wl,-M,-Map,build/$(PROJECT_NAME).map -T $^ -o $@

build/%.raw: build/%.elf
	$(OBJCOPY) -S -I elf32-littlearm -O binary $< $@
	$(SIZE) --target=binary $<

build/%.dis: build/%.elf
	$(OBJDUMP) -S -j .text $< > $@ || rm $@

build/%.bin: build/%.raw
	tools/mkimage.py $< $@

.PHONY: clean
clean:
	rm -rf build
