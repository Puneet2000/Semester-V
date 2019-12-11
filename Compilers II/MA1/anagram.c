#include<stdio.h>
int main(){
	char s1[100],s2[100];
	scanf("Strings %s %s",s1,s2);
	int a[26] = {0};
	int i;
	for (i=0;s1[i]!='\0';i++)
		a[s1[i]-'a']++;

	for (i=0;s2[i]!='\0';i++)
		a[s2[i]-'a']--;
	int anagram = 1;
	for(i=0;i<26;i++){
		if(a[i]!=0){
			anagram=0;
			break;
		}
	}

	if (anagram==1)
		printf("Anagram\n");
	else
		printf("Not Anagram\n");
	return 0;
}