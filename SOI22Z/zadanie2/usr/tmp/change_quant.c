#include <lib.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
	message m;
	m.m1_i1 = 1; /* group */
	m.m1_i2 = atoi(argv[1]); /* new quant value */
	
	_syscall(MM, SETQUANT, &m);
	
	m.m1_i1=2;
	m.m1_i2=atoi(argv[2]);

	printf("Changing quantum, group 1: %d, group 2:%d\n",atoi(argv[1]),atoi(argv[2]));
	_syscall(MM,SETQUANT,&m);
	return 0;
}

