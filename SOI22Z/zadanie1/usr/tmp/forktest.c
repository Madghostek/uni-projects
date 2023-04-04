#include <lib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h> /* sleep */
#include <stdlib.h> /* exit */

int CreateChain(int chainLength)
{
	int pid; /* pid of process that is supposed
			  to be at the end of the chain (last child)*/
	int i;

	for (i=0; i<chainLength; ++i)
	{
		pid = fork();
		if (pid)
		{
			/* parent */
			sleep(2);
			exit(0);
		}
	}

	return getpid();
	
}

int main(int argc, char* argv[] )

{
	int lastChild;
	int res, respid, requested;
	message m;
	
	printf("Generating chain of length %s\n", argv[1]);
	requested = atoi(argv[1]);
	lastChild = CreateChain(requested);
	/* this code is executed by last child in chain */
	res =_syscall(MM, GETLCHN, &m);
	respid = _syscall(MM, GETLCHNPID, &m);
	printf("Syscall result (lognest pid, length): %d, %d, errno :%d, (%s)\n\n", respid, res, errno, strerror(errno));
	printf("last child was: %d\n",lastChild);
	return 0;
}
