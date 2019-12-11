#include<stdio.h>

int main(){
	unsigned int n;
	scanf("%u",&n);
	int i;
	int prime =1;
	for(i=2;i*i<=n;i++){
		if (n%i == 0){
			prime =0;
			break;
		}
	}
	if(prime==1)
		printf("Number is prime\n");
	else
		printf("Number is composite\n");
	return 0;
}