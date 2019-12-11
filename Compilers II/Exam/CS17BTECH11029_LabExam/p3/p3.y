%define parse.error verbose
%{
	#include<stdio.h>
	#include<stdlib.h>
	using namespace std;
	extern int yylex();
	void yyerror(const char*s);
%}
%union {int d;}
%token PAPER ROCK SCISSORS NUM NUM_MOVES OP LINE DIGIT PLAYER
%type<d> DIGIT PLAYER
%start S

%%
    S   : NUM OP DIGIT  LINE NUM_MOVES OP DIGIT player_moves LINE matches;
    player : PLAYER;
    player_moves : LINE player_move  player_moves | player_move;
    player_move : player OP moves;
    moves : move moves | move;
    move : ROCK | PAPER | SCISSORS;
    matches : player matches | player;

%%

void yyerror(const  char *s){
	printf("%s",s);
	exit(1);
}

int main(){
	yyparse();
	return 0;
}
