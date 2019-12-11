%define parse.error verbose
%{
	#include<stdio.h>
	#include<stdlib.h>
	#include<iostream>
	#include<algorithm>
	using namespace std;
	extern int yylex();
	void yyerror(const char*s);
	int x=0;
	int y=0;
	int x_corr[2];
	int y_corr[2];
	int x_curr[2];
	int y_curr[2];
	string op="none";
	int c = 0;
	void check(){
		if (c<=1){
			x_curr[0] = x_corr[0];
			x_curr[1] = x_corr[1];
			y_curr[0] = y_corr[0];
			y_curr[1] = y_corr[1];
		}
		else{
			if (op=="u"){
				x_curr[0] =  min(x_curr[0],x_corr[0]);
				x_curr[1] =  max(x_curr[1],x_corr[1]);
				y_curr[0] =  min(y_curr[0],y_corr[0]);
				y_curr[1] =  max(y_curr[1],y_corr[1]);
			}
			else if (op=="n"){
				x_curr[0] =  max(x_curr[0],x_corr[0]);
				x_curr[1] =  min(x_curr[1],x_corr[1]);
				y_curr[0] =  max(y_curr[0],y_corr[0]);
				y_curr[1] =  min(y_curr[1],y_corr[1]);
			}

			//printf("%d %d %d %d\n", x_curr[0],x_curr[1],y_curr[0],y_curr[1]);

			for(int i=y;i>=0;i--){
				cout<<i<<"|";
				for(int j=0;j<=x;j++){
					if (y_curr[0]<=i && i<=y_curr[1] && x_curr[0]<=j && j<=x_curr[1]){
						cout<<"x ";
					}
					else{
						cout<<"  ";
					}
				}
				cout<<endl;
			}
			cout<<" ";
			for(int i=0;i<=x;i++){
				cout<<"_"<<" ";
			}
			cout<<endl<<" ";
			for(int i=0;i<=x;i++){
				cout<<i<<" ";
			}

			cout<<endl<<endl;
		}


	}
%}
%union {int d; char ch;}
%token INST UNION X Y LESS LEQ DIGIT LINE OPEN CLOSE SEP
%type<d> DIGIT
%type<s> X Y
%start S

%%
    S   : DIGIT {x=$1;} DIGIT {y=$3;} LINE program;
    program : poly {c++; check();} op program | poly {c++; check();};
    op : INST {op="n";} | UNION {op="u";};
    poly : OPEN constraint_list CLOSE;
    constraint_list : constraint SEP constraint_list | constraint;
    constraint : DIGIT ie X ie DIGIT {x_corr[0] = $1; x_corr[1]=$5;} | DIGIT ie Y ie DIGIT {y_corr[0] = $1; y_corr[1]=$5;} | DIGIT ie X SEP Y ie DIGIT {x_corr[0] = $1; x_corr[1]=$7; y_corr[0] = $1; y_corr[1]=$7;};
    ie : LESS | LEQ;

%%

void yyerror(const  char *s){
	printf("%s",s);
	exit(1);
}

int main(){

	yyparse();
	return 0;
}
