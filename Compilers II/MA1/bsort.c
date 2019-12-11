#include <stdio.h> 
void swap(int *xp, int *yp)  
{  
    int temp = *xp;  
    *xp = *yp;  
    *yp = temp;  
}  

void sort(int arr[], int n)  
{  
    int i, j;  
    for (i = 0; i < n-1; i++)      
        for (j = 0; j < n-i-1; j++)  
            if (arr[j] > arr[j+1])  
                swap(&arr[j], &arr[j+1]);  
}  

int main()  
{  
    int len=50000;
    // scanf("%d",&len);
    // int arr[len];
    // int i;
    // for(i=0;i<len;i++)
    //     scanf("%d",&arr[i]);    
    // sort(arr, len);  
    // for(i=0;i<len;i++)
    //     printf("%d ",arr[i]);
    // printf("\n");
    int a[len];
    int i;
    for (i=0;i<len;i++)
        a[i] = len-i;
    sort(a,len);
    return 0;  
}  
  