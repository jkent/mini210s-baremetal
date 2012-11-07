#include <linux/compiler.h>
#include <asm/system.h>

#define STACK_BASE 0xD0035400
#define STACK_SIZE (3<<10)

#define GPJ2CON *((volatile unsigned int *) 0xE0200280)
#define GPJ2DAT *((volatile unsigned int *) 0xE0200284)
#define GPJ2PUD *((volatile unsigned int *) 0xE0200288)
#define GPJ2DRV *((volatile unsigned int *) 0xE020028C)

static inline void disable_l2_cache()
{
	unsigned int val;
	asm volatile ("mrc p15, 0, %0, c1, c0, 1" : "=r" (val) : : "cc");
	val &= ~0x2;
	asm volatile ("mcr p15, 0, %0, c1, c0, 1" : : "r" (val) : "cc");
}

static inline void setup_l2_cache()
{
	unsigned int val;
	asm volatile ("mrc p15, 1, %0, c9, c0, 2" : "=r" (val) : : "cc");
	/* 2 cycle L2 data RAM read multiplexer
	 * disable parity/ecc
	 * 2 cycle tag ram latency
	 * 2 cycle data ram latency
	 */
	val &= ~0x202001C7;
	asm volatile ("mcr p15, 1, %0, c9, c0, 2" : : "r" (val) : "cc");
}

static inline void enable_l2_cache()
{
	unsigned int val;
	asm volatile ("mrc p15, 0, %0, c1, c0, 1" : "=r" (val) : : "cc");
	val |= 0x2;
	asm volatile ("mcr p15, 0, %0, c1, c0, 1" : : "r" (val) : "cc");
}

static inline void invalidate_cache()
{
	unsigned int val = 0;
	/* Invalidate Inst-TLB and Data-TLB */
	asm volatile ("mcr p15, 0, %0, c8, c7, 0" : : "r" (val) : "cc");
	/* Invalidate all instruction caches to point of unification.
	 * Also flush branch target cache.
	 */
	asm volatile ("mcr p15, 0, %0, c7, c5, 0" : : "r" (val) : "cc");
}

void __naked __section(.text_entry) start(void)
{
	asm volatile (
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
	unsigned int val;

	/* supervisor mode */
	asm volatile ("msr CPSR_c, #0xd3");

	disable_l2_cache();
	setup_l2_cache();
	enable_l2_cache();
	invalidate_cache();

	val = get_cr();
	/* Normal exception vectors
	 * Data caching disabled at all levels
	 * MMU disabled
	 * Program flow prediction enabled
	 * Strict alignment fault checking enabled
	 */
	val &= ~(CR_V | CR_C | CR_M);
	val |= (CR_Z | CR_A);
	set_cr(val);

	asm volatile (
		"ldr sp, =%c0\n"
		"mov fp, #0\n"
		: : "i"(STACK_BASE + STACK_SIZE - 12)
	);

	GPJ2CON = (GPJ2CON & 0xFFFF0000) | 0x00001111;
	GPJ2DAT = (GPJ2DAT & 0xFFFFFFF0) | 0x0000000E;
	GPJ2PUD = (GPJ2PUD & 0xFFFFFF00);
	GPJ2DRV = (GPJ2DRV & 0xFFFFFF00) | 0x000000FF;

	while (1)
		;
}
