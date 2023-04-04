;  ARKO 21L project x86 - black white conversion

	SECTION .data
magic:		dq 0x0000001500480007	; 7 R, 0x48=72 G, 0x15=21 B, 00 for rest

	SECTION .text
        global convert  ; must be with underscore on windows
convert:
	; stack after init (ebp offset):
	;esp-> -0xC: saved ebx
	;	   -0x8: saved esi
	;	   -0x4: saved edi
	;ebp->  0x0: old ebp
	;		0x4: return address
	;		0x8: pointer to ImageInfo
	;		0xC: rect_left				]
	;		0xE: rect_top				] convert info structure (defined in main.c)
	;		0x10: rect_right			] passing the struct by value allows to modify it freely,
	;		0x12: rect_bottom			] and reduces pointer dereferences.
	;		0x14: threshold				] 

	; function init
	push ebp
	mov ebp,esp
	push edi
	push esi
	push ebx 

	; prevent invalid bounds
	mov esi, [ebp+0x8]			; esi = imgInfo address

	;;;;;;;;;debug
	;mov [esi+0xC],dword 0
	;;;;;;;;;;;;;;

	; width
	movzx ebx, word [esi] 		; image width, moving only 16 bits, so movzx
	lea ebx, [ebx-1]			; !image size must be subtracted by 1, because rect is 0-indexed
	movzx ecx, word [ebp+0x10] 	; rect_right
	cmp bx, cx 					; if width<rect_right...
	cmovb cx, bx 				; width=rect_right
	mov [ebp+0x10], cx

	; height
	movzx ebx, word [esi+0x4]
	lea ebx, [ebx-1]
	movzx ecx, word [ebp+0xE]
	cmp bx, cx
	cmovb cx, bx
	mov [ebp+0xE], cx

	; right now esi = imgInfo, no other register is used


	; get starting address and end address (for current line) at once
	; later, the loop will be running until current==end

	;unsigned char* pixels = info->pImg+info->line_bytes*rect.rect_bottom; 

	mov ebx, [esi+0x8]			; line size in bytes, this will be useful later
	movzx eax, word [ebp+0x12]	;rect_bottom
	mul bx						; multiply both to get starting y offset 
	; result is in dx:ax, so dx must be moved to upper half of eax
	; this is done with ecx and shift
	mov ecx, eax
	mov ax,dx
	shl eax, 16
	mov ax,cx
	add eax,[esi+0xC]			;+pImg, eax now contains starting line address

	;unsigned  char * line_end_ptr = pixels+rect.rect_right*3+3;

	movzx ecx, word [ebp+0x10]	;rect_right
	lea ecx, [ecx*2+ecx]
	lea ecx, [ecx+3]	;ecx=rect_right*3+3, save for end address
	lea edx, [eax+ecx]	;edx = end pixel address

	;pixels+=+rect.rect_left*3;

	movzx edi, word [ebp+0xC]	;rect_left
	lea edi, [edi*2+edi];*3		;*3
	add eax, edi 		;add to line address, eax now holds starting pixel address

	;unsigned delta_between_lines = rect.rect_left*3+info->line_bytes-rect.rect_right*3-3;
	add edi, ebx	;rect_left*3+line_bytes
	sub edi, ecx 	;...-(rect_right*3+3), edi = delta_between_lines

	; cx will be line counter, load it with rect_bottom
	mov cx, word [ebp+0x12]

	; multiply threshold by 100
	movzx ebx, byte [ebp+0x14]
	lea ebx, [ebx*4+ebx]	;*5
	lea ebx, [ebx*4+ebx]	;*5
	shl ebx, 2				;*2 = 100, ebx=threshold*100

	; everything so far:
	; eax = start pixel address
	; ebx = threshold
	; ecx = line counter (bottom->top)
	; edx = end pixel address
	; edi = amount of bytes between end and next pixel
	; esi = pointer to ImgInfo

	; save edi on stack because there are no registers left
	push edi

	; edi will be used as temp register for obtaining RGB value

	
	; loop start
	MOVQ xmm0, [magic]
	; calculate current pixel value, load the rgb first
loop_start:
	mov edi, [eax]
	; edi = 0x00RRGGBB			; PMADDWD:
	PXOR xmm1, xmm1				; xmm0 ...|0000|0015|0048|0007|
	PINSRB xmm1, edi, 0         ;		    *    *	  *	   *
	shr edi, 8                  ; xmm1 ...|0000|00RR|00GG|00BB|
	PINSRB xmm1, edi, 2         ;			=    =    =    =
	shr edi, 8					;			0    21R  72G  7B
	PINSRB xmm1, edi, 4         ;			   +    |    +
								;	= ... |   21R   | 72G+ 7B |
	PMADDWD xmm1, xmm0			;PHADDD: suma 32 bitowych sektorow, czyli xmm1=21R+72G+7B
	PHADDD xmm1, xmm1
	MOVD edi, xmm1	; move result from xmm1

	cmp edi, ebx ; threshold is in ebx
	ja write_white
	; write black to pixel address
	mov [eax], word 0xFFFF
	mov [eax+2], byte 0xFF
	jmp after_write
write_white:
	mov [eax], word 0x0
	mov [eax+2], byte 0x0
after_write:
	; increment pixel by 3
	lea eax, [eax+3]
	cmp eax,edx
	jne loop_start
	
	; increment line counter, add delta to current pixel address,
	; add whole line length to end address, check if above rect_top
	inc cx
	add edx, [esi+0x8]
	add eax, [esp]	; delta is on stack
	cmp cx, word [ebp+0xE]
	jna loop_start

	; restore registers
	add esp, 4 ; discard the thing pushed earlier
	pop ebx
	pop esi
	pop edi
	pop ebp
	ret
