%define parse.error verbose
%{
	#include<stdio.h>
	#include<stdlib.h>
	#include<iostream>
	#include<vector>
	using namespace std;
	extern int yylex();
	void yyerror(const char*s);

	struct row {
		int valid = 0;
		string target="";
		string prot="all";
		string source="anywhere";
		string dest="anywhere";
	};

	struct row curr_row;
	string chain="";
	string op= "";
	int pos=0;
	string policies[] = {"ACCEPT","ACCEPT","ACCEPT"};
	struct row input[1000];
	struct row output[1000];
	struct row forw[1000];
	void run(){
		if (op=="insert"){
			curr_row.valid = 1;
			if (chain=="INPUT")
				input[pos] = curr_row;
			else if (chain == "OUTPUT")
				output[pos] = curr_row;
			else if (chain == "FORWARD")
				forw[pos]= curr_row;
		}
		else if (op == "delete"){
			if (chain=="INPUT")
				input[pos].valid = 0;
			else if (chain == "OUTPUT")
				output[pos].valid = 0;
			else if (chain == "FORWARD")
				forw[pos].valid = 0;
		}
		else if (op == "replace"){
			curr_row.valid = 1;
			if (chain=="INPUT")
				input[pos] = curr_row;
			else if (chain == "OUTPUT")
				output[pos] = curr_row;
			else if (chain == "FORWARD")
				forw[pos] =  curr_row;
		}
		else if (op == "policy"){
			if (chain=="INPUT")
				policies[0] = curr_row.target;
			else if (chain == "OUTPUT")
				policies[1] = curr_row.target;
			else if (chain == "FORWARD")
				policies[2] = curr_row.target;
		}

		struct row new_row;
		curr_row =  new_row;
		chain = "";
		pos = 0;
		op = "";
	}
%}
%union {int d; char* s;}
%token INSERT DELETE REPLACE POLICY OUTPUT INPUT FORWARD TCP UDP ACCEPT DROP DIGIT LINE IPTABLE IP SOURCE DEST PROTOCOL TARGET
%type<d> DIGIT
%type<s> IP
%start S

%%
    S   : command { run();} LINE S | command { run(); };
    chain : INPUT {chain = "INPUT";} | OUTPUT {chain = "OUTPUT";} | FORWARD {chain = "FORWARD";};
    target :  DROP {curr_row.target = "DROP";} | ACCEPT {curr_row.target = "ACCEPT";};
    prot : UDP {curr_row.prot = "udp";} | TCP {curr_row.prot == "tcp";};
    option : SOURCE IP {curr_row.source = $2;}
    		| DEST IP {curr_row.dest = $2;}
    		| TARGET target 
    		| PROTOCOL prot;
    option_list : option option_list | option
    command : delete | change_p | replace | insert;
    delete : IPTABLE DELETE {op="delete";} chain DIGIT {pos =$5;};
    change_p : IPTABLE POLICY {op="policy";} chain target;
    replace : IPTABLE REPLACE {op="replace";} chain DIGIT {pos =$5;} option_list;
    insert : IPTABLE INSERT {op="insert";} chain DIGIT {pos =$5;} option_list;

%%

void yyerror(const  char *s){
	printf("%s",s);
	exit(1);
}

int main(){
	yyparse();

	cout<<"Chain INPUT (policy "<<policies[0]<<")\n";
	printf("target\tprot\tsource\tdestination\n");
	for (int i=0;i<1000;i++){
		if (input[i].valid==1)
			cout<<input[i].target<<"\t"<<input[i].prot<<"\t"<<input[i].source<<"\t"<<input[i].dest<<endl;
	}
	printf("\n");
	cout<<"Chain FORWARD (policy "<<policies[2]<<")\n";
	printf("target\tprot\tsource\tdestination\n");
	for (int i=0;i<1000;i++){
		if (forw[i].valid==1)
			cout<<forw[i].target<<"\t"<<forw[i].prot<<"\t"<<forw[i].source<<"\t"<<forw[i].dest<<endl;
	}
	printf("\n");
	cout<<"Chain OUTPUT (policy "<<policies[1]<<")\n";
	printf("target\tprot\tsource\tdestination\n");
	for (int i=0;i<1000;i++){
		if (output[i].valid==1)
			cout<<output[i].target<<"\t"<<output[i].prot<<"\t"<<output[i].source<<"\t"<<output[i].dest<<endl;
	}
	return 0;
}
