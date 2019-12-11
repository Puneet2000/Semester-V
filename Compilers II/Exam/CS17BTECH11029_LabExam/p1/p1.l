%{
	#include<stdio.h>
	#include<stdlib.h>
	#include"y.tab.h" 
%}

%%

(?i:iptables) {return IPTABLE;}
"-D" {return DELETE;}
"-I" return INSERT;
"-R" return REPLACE;
"-P" return POLICY;
"-s" return SOURCE;
"-d" return DEST;
"-j" return TARGET;
"-p" return PROTOCOL;

"OUTPUT"	{ 
			 return OUTPUT;}
"INPUT" 	{ 
			 return INPUT;}
"FORWARD" 	{ 
			 return FORWARD;}
"tcp" 	{
			 return TCP;}	
"udp"	{
			 return UDP;}		 
"DROP" {
			 return DROP;}

"ACCEPT" {
			 return ACCEPT;}

[0-9] { yylval.d = atoi(yytext);
		return DIGIT;}

[0-9]"."[0-9]"."[0-9]"."[0-9] {yylval.s = yytext;
		return IP;}
                                         ;
" "  ;
"\n" {return LINE;}
. 		;

%%

int yywrap(void){
	return 1;
}

