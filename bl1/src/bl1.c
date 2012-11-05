#define notrace				__attribute__((no_instrument_function))
#define __naked				__attribute__((naked)) notrace
#define __section(S)		__attribute__ ((__section__(#S)))

#define GPJ2CON *((volatile unsigned int *) 0xE0200280)
#define GPJ2DAT *((volatile unsigned int *) 0xE0200284)
#define GPJ2PUD *((volatile unsigned int *) 0xE0200288)
#define GPJ2DRV *((volatile unsigned int *) 0xE020028C)

void __naked __section(.text_entry) start(void)
{
	__asm__ __volatile__ (
		"b reset\n"
		"1: b 1b\n"
		"1: b 1b\n"
		"1: b 1b\n"
		"1: b 1b\n"
		"1: b 1b\n"
		"1: b 1b\n"
		"1: b 1b\n"
	);

}

void __naked __section(.text_init) reset(void)
{

	GPJ2CON = (GPJ2CON & 0xFFFF0000) | 0x00001111;
	GPJ2DAT = (GPJ2DAT & 0xFFFFFFF0) | 0x0000000E;
	GPJ2PUD = (GPJ2PUD & 0xFFFFFF00);
	GPJ2DRV = (GPJ2DRV & 0xFFFFFF00) | 0x000000FF;

	__asm__ __volatile__ (
	    "1: b 1b\n"
	);
}
