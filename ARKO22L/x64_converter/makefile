CC=gcc
ASMBIN=nasm

all : asm cc link
asm : 
	$(ASMBIN) -o converter.o -f elf64 -g -l converter.lst converter.asm
cc :
	$(CC) -m64 -c -g -O0 main.c image.c
link : converter.o
	$(CC) -m64 -g -o program main.o converter.o image.o

clean :
	rm -f *.o
	rm -f program
	rm -f errors.txt	
	rm -f converter.lst
