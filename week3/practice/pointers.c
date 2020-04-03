#include<stdio.h>


void swapping(int *cptr, int *dptr) {
	int tmp;
	tmp = *cptr;
	*cptr = *dptr;
	*dptr = tmp;
	printf("In function: %d %d\n", *cptr , *dptr);
	}


int main(void)	{
    int x;
	int *ptr_p;
	x = 5;

    ptr_p = &x;
	printf("1: %d\n", *ptr_p);

    int a,b;

	a=5;
	b=10;
	printf("input: %d %d\n", a, b);
	swapping(&a,&b); // & operator is used to get the variable's address
	// think of * as 'value present at address' and '&' as address of
	printf("output: %d %d\n", a, b);


	// pointers and arrays
	char array[10];

	char *arrayptr = &array[0]; // array ptr is now same as first element in array
	printf("1st array element: %d\n", *arrayptr);

	int z = 27; // declare variable z and set equal to 27
	int *zptr = &z; // declare pointer and set to address of z

	printf("I pointed to Z: %d.\n This is the same as Z: %d.", *zptr, z);

    return 0;

	}