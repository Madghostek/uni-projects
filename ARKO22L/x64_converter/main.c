#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "image.h"

typedef struct {
	uint16_t rect_left; 	//0x0
	uint16_t rect_top;		//0x2
	uint16_t rect_right;	//0x4
	uint16_t rect_bottom;	//0x6
	uint8_t threshold;		//0x8

} SConvert_info;

SConvert_info params;

extern void __attribute__((sysv_abi)) asm_convert(unsigned char* pixels, unsigned char* region_line_end, uint16_t delta, uint16_t rect_top, uint16_t threshold, int line_length);

void convert_wrapper(const ImageInfo*, SConvert_info);

int main()
{
	ImageInfo* info = readBmp("source.bmp");
	if (info==NULL) goto end;
	

	// specify region to convert, bounds are inclusive
	params.rect_left = 0;
	params.rect_top = 1000;
	params.rect_right = 1000;
	params.rect_bottom = 0;
	params.threshold = 80;
	// pass a copy of params, but a pointer to image info
	convert_wrapper(info, params);
	saveBmp("output.bmp", info);
end:
	freeImage(info);
	return 0;
}


// this time more work is done on C side, only the critical loop is done in assembly
void convert_wrapper(const ImageInfo* info, SConvert_info rect)
{
	// limit bounds
	if (rect.rect_top>=info->height) rect.rect_top=info->height-1;
	if (rect.rect_right>=info->width) rect.rect_right=info->width-1;

	// prepare intial values for the loop:
	// starting address, end address (on first line), amount to add between iterations

	unsigned char* pixels = info->pImg + info->line_bytes*rect.rect_bottom; // starting line address
	unsigned char* region_line_end = pixels+rect.rect_right*3+3; 				// address of first pixel past rect_right bound
	pixels+=+rect.rect_left*3;												// now pixels holds address of starting pixel
	uint16_t delta_between_lines = rect.rect_left*3+info->line_bytes-rect.rect_right*3-3;

	// there is no need to pass whole rect structure now, but still 6 values are needed
	// rdi - pixels
	// rsi - region_line_end
	// rdx - delta_between_lines
	// rcx - rect_top
	// r8d - threshold
	// r9d - line length in bytes
	asm_convert(pixels, region_line_end, delta_between_lines, rect.rect_top-rect.rect_bottom+1, rect.threshold*100, info->line_bytes);
}
