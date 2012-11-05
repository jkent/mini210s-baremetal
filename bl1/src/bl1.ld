OUTPUT_FORMAT("elf32-littlearm", "elf32-littlearm", "elf32-littlearm")
OUTPUT_ARCH(arm)
ENTRY(start)
SECTIONS
{
	. = 0xD0020010;

	. = ALIGN(4);
	.text      :
	{
		_stext = .;
		_text = .;
		*(.text_entry*)
		__init_start = .;
		*(.text_init*)
		__init_end = .;
		*(.text*)
	}

	_init_size = __init_end - _text;

	. = ALIGN(4);
	.rodata : { *(.rodata*) }

	_etext = .;			/* End of text and rodata section */

	. = ALIGN(4);
	.data : { *(.data*) }

	. = ALIGN(4);
	__bss_start = .;
	.bss : { *(.bss*) }
	__bss_stop = .;
	_end = .;
}
