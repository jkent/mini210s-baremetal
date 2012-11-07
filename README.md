Mini210s Baremetal
==================

Currently various bits and pieces.  Eventually will have something that can load a binary from a FAT filesystem on a SD card and then execute it.  After that a barmetal Lua environment will be implemented.

Getting started
---------------

We're going to assume you are using a Linux system for development.  For development, you'll want to create a udev rule to give you permission to talk to the USB DNW interface.

Create the file `/etc/udev/rules.d/99-dnw.rules` with the following contents:

    ATTRS{idVendor}=="04e8", ATTRS{idProduct}=="1234", MODE="666"

### Building

Make sure you have an arm-none-eabi toolchain in your path, and type `make`.  If you need an arm-none-eabi toolchain, there is [Mentor Graphics CodeBench Light].  It is unfortunately behind a registration wall.

  [Mentor Graphics CodeBench Light]: http://www.mentor.com/embedded-software/sourcery-tools/sourcery-codebench/editions/lite-edition/ 

### Running

There are two ways to run code, `bl1.bin` can be written to the second 512 byte block of an sd card, or you can load it via USB.  We'll only go into the details of the later for now.  First, you'll want to put your board int SD boot mode and then remove any MicroSD card you might have inserted.  The Mini210s will first try to boot off SD, then UART, and then failing that, it will attempt to USB boot, but only if you have a Micro-B cable connected to your development machine.

##### Debug Server

Run `make server` and then turn your board on.  The latest build of `bl1.bin` will automatically be sent to your device as soon as it enumerates.  This is convenient for active development.

##### Single Load

Turn on your board, and then run `make load`.

