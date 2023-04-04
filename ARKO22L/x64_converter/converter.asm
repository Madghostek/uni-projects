;  ARKO 21L project x86 - black white conversion

	SECTION .rodata
magic:		dq 0x0000001500480007	; 7 R, 0x48=72 G, 0x15=21 B, 00 for rest

	SECTION .text
        global asm_convert
asm_convert:
	; rdi - pixels
	; rsi - region_line_end
	; rdx - delta_between_lines
	; rcx - amount of lines to convert
	; r8d - threshold
	; r9d - line length in bytes

	; loop start
	MOVQ xmm0, [rel magic]	; this means relative to rip, because gcc compiles position independend binary by default

loop_start:
	mov r10d, [rdi]
	; r10d = 0x00RRGGBB			; PMADDWD:
	PXOR xmm1, xmm1				; xmm0 ...|0000|0015|0048|0007|
	PINSRB xmm1, r10d, 0         ;		    *    *	  *	   *
	shr r10d, 8                  ; xmm1 ...|0000|00RR|00GG|00BB|
	PINSRB xmm1, r10d, 2         ;			=    =    =    =
	shr r10d, 8					;			0    21R  72G  7B
	PINSRB xmm1, r10d, 4         ;			   +    |    +
								;	= ... |   21R   | 72G+ 7B |
	PMADDWD xmm1, xmm0			;PHADDD: suma 32 bitowych sektorow, czyli xmm1=21R+72G+7B
	PHADDD xmm1, xmm1
	MOVD r10d, xmm1	; move result from xmm1

	cmp r10d, r8d ; threshold is in r8d
	ja write_black
	; write black to pixel address
	mov [rdi], word 0xFFFF
	mov [rdi+2], byte 0xFF
	jmp after_write
write_black:
	mov [rdi], word 0x0
	mov [rdi+2], byte 0x0
after_write:
	; increment pixel by 3
	lea rdi, [rdi+3]
	cmp rdi,rsi
	jne loop_start
	
	; increment line counter, add delta to current pixel address,
	; add whole line length to end address, check if above rect_top
	dec cx
	add rdi, rdx	; pixels+=delta
	add rsi, r9	; region_end+line length = end of next line
	test cx, cx		; lines left to convert == 0?
	jnz loop_start
	ret
