
======================================
Socket Programming Assignment
	- Puneet Mangla (CS17BTECH11029)
======================================

## Requirements : 

	1. python 2.7 
	2. threading library
	3. socket library
======================================

## Q1. Add two features to Echo Client /Server, and demonstrate them.

- Run server : ``` python server.py --port [PORT] ```
- Run client : ``` python client.py --ip [IP] --port [PORT]
- Download a file : ``` downlaod <file_name> ```
- Execute a command : ``` run <command> ```
- Close connection : ```close``
====================================================================

## Q2. HARD Mode: 1 server and N clients.

- Run server : ``` python server.py --port [PORT] ```
- Run client : ``` python client.py --ip [IP] --port [PORT] --lp [CLIENT PORT] --uname [USERNAME]
- Send message : ``` <message> |<username>```
- Received message will look like : ``` <username>| <message>```
- Close connection : ```close``
====================================================================

## Q3. Client and server to be protocol independent (support both IPv4 and IPv6).

- Run server : ``` python server.py --port [PORT] ```
- Run client : ``` python client.py --ip [ipv6/ipv4] --port [PORT]
- Download a file : ``` downlaod <file_name> ```
- Execute a command : ``` run <command> ```
- Close connection : ```close``
====================================================================

