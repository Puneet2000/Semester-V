%{
	#include<stdio.h>
	#include<stdlib.h>
	#include"y.tab.h" 
%}

%%

"P"[1-9][0-9]* { yylval.d = atoi(yytext++);
				return PLAYER;

}
[1-9][0-9]* { yylval.d = atoi(yytext);
				return DIGIT;

}
"P" return PAPER;
"R" return ROCK;
"S" return SCISSORS;
"N" return NUM;
"K" return NUM_MOVES;
"==" return OP;                                 ;
" "  ;
"\n" {return LINE;}
. 		;

%%

int yywrap(void){
	return 1;
}

