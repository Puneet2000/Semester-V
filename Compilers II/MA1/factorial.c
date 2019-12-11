#include<stdio.h>
unsigned int factorial(unsigned int n){
	if(n==1 || n==0)
		return 1;
	else
		return n*factorial(n-1);
}

int main(){
	unsigned int n;
	scanf("%u",&n);
	printf("Factorial of %u is %u\n",n,factorial(n));
	return 0;
}