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

// takes pointer to parameters structure
extern void convert(const ImageInfo*, SConvert_info);
void convert_C(ImageInfo*, SConvert_info);

int main()
{
	ImageInfo* info = readBmp("source.bmp");
	if (info==NULL) goto end;
	
	//xd(info);
	// specify region to convert, bounds are inclusive
	params.rect_left = 0;
	params.rect_top = 10000;
	params.rect_right = 10000;
	params.rect_bottom = 0;
	params.threshold = 80;
	convert(info, params);
	saveBmp("output.bmp", info);
end:
	freeImage(info);
	return 0;
}






void __attribute__ ((noinline)) convert_C(ImageInfo* info, SConvert_info rect)
{
	if (rect.rect_top>=info->height) rect.rect_top=info->height-1;
	if (rect.rect_right>=info->width) rect.rect_right=info->width-1;
	rect.threshold*=100;

	unsigned char* pixels = info->pImg + info->line_bytes*rect.rect_bottom; 
	unsigned  char * line_end_ptr = pixels+rect.rect_right*3+3; //address of first pixel past rect_right
	pixels+=+rect.rect_left*3;
	unsigned delta_between_lines = rect.rect_left*3+info->line_bytes-rect.rect_right*3-3;

	/*printf("rect %d %d %d %d\n",rect.rect_left,rect.rect_top,rect.rect_right,rect.rect_bottom);
	printf("info: h:%d, w:%d, line_bytes:%d\n",info->width, info->height, info->line_bytes);
	printf("%p, %p, %d",pixels,line_end_ptr, delta_between_lines);*/

	for (unsigned y = rect.rect_bottom; y<=rect.rect_top; ++y)
	{

		while (pixels!=line_end_ptr)
		{
			unsigned value = pixels[0]*7+pixels[1]*72+pixels[2]*21;
			if (value<=rect.threshold)
			{
				memset(pixels,0xFF,3);
			}
			else
			{
				memset(pixels,0x00,3);
			}
			pixels+=3;
				
		}
		pixels+=delta_between_lines;
		line_end_ptr+=info->line_bytes;
	}
}






// void test(ImageInfo* info)
// {
// 	params.threshold = 210;
// 	short argsx[] = {10, 30, 10, 20, 30, 50, 60, 70, 60, 50, 50};
// 	short argsy[] = {10, 30, 30, 20, 10, 30, 30, 20, 10, 10, 20};
// 	for (int i=0; i<sizeof(argsx)/sizeof(short);++i)
// 	{
// 		params.rect_left = argsx[i];
// 		params.rect_top = argsy[i]+10;
// 		params.rect_right = argsx[i]+10;
// 		params.rect_bottom =argsy[i];
// 		convert(info, params);
// 	} 
// }