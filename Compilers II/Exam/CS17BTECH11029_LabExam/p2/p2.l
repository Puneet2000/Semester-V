%{
	#include<stdio.h>
	#include<stdlib.h>
	#include"y.tab.h" 
%}

%%

"n" return INST;
"u" return UNION;
"x" return X;
"y" return Y;
"{" return OPEN;
"}" return CLOSE;
"," return SEP;

"<" return LESS;
"<=" return LEQ;
[1-9][0-9]* { yylval.d = atoi(yytext);
				return DIGIT;

}
                                         ;
" "  ;
"\n" {return LINE;}
. 		;

%%

int yywrap(void){
	return 1;
}

