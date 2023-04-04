#include <lib.h>
#include <unistd.h>
#include <stdio.h>

void VeryLongLoop(void)
{
	int i,j;
	volatile int v;
	for (i=0; i<1000000;++i)
	{
		for (j=0;j<1000000;++j)
		{
			v=i+j;
		}
	}
}

int main(void)
{
	pid_t pid;
	message m;

	pid = fork();

	if (pid==0)
	{
		printf("I'm child\n");
		/* child */
		m.m1_i1 = getpid(); /* process pid to change the group of */
		m.m1_i2 = 1; /* new group identifier (0,1 or 2) */
		_syscall(MM, SETGROUP, &m);
		
		
		pid = fork();
		if (pid==0)
			fork();

		printf("three group 1 processes start loop\n");
		VeryLongLoop();
		
		printf("child end\n");
	}
	else
	{
		/* parent */
		printf("im parent\n");
		m.m1_i1 = getpid(); /* process pid to change the group of */
		m.m1_i2 = 2; /* new group identifier (0,1 or 2) */
		_syscall(MM, SETGROUP, &m);

		fork();

		printf("two group 2 processes start loop\n");
		VeryLongLoop();

		printf("parent end\n");
	}
	return 0;
}
