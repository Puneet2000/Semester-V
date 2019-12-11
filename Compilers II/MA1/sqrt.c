#include<stdio.h>
int main()
{
	float x;
	scanf("%f",&x);
	float lo =0.0, hi=x;
	while (hi-lo> 1e-4){
		float mid = lo + (hi-lo)/2;
		if (mid*mid>x)
			hi = mid;
		else
			lo = mid;
	}

	printf("Square root is %f \n",lo);

	return 0;
}