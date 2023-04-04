#include <lib.h>
#include <unistd.h>
#include <stdio.h>


int main()
{
	int i, group1,group2;
	message m;
	for (i=0;i<10;++i)
	{
		m.m1_i1=1;
		group1=_syscall(MM, GETUTIME, &m);

		m.m1_i1=2;
		group2=_syscall(MM, GETUTIME, &m);
		
		printf("group 1 / group 2: %d / %d\n", group1, group2);
		sleep(1);
	 	/* goes over all processes, if group is 1, adds to gorup1 counter*/
	}
	return 0;
}