import socket # for socket 
import argparse
import threading, thread
import os
def receive(s): # receive and print message in console
	while True:
		res = s.recv(4096).decode()
		print(res)
		if res == 'Closing..':
			break
	s.close()
	os._exit(0)
	return
parser = argparse.ArgumentParser()

parser.add_argument('--ip', type=str,  # server IP
                    help='IP Addr') 
parser.add_argument('--port', type=int, # server port
                    help='server port')
parser.add_argument('--lp', type=int, # self binding port
                    help='self listening port')
parser.add_argument('--uname', type=str, # usrname
                    help='username')


args = parser.parse_args()

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket 
except socket.error as err: 
    print ("socket creation failed with error %s" %(err)) 

s.bind(('127.0.0.1', args.lp))
s.connect((args.ip, args.port))  # connect them
s.sendall(args.uname.encode())
msg = s.recv(4096)
print(msg.decode())

t1=threading.Thread(target=receive,args=(s,)) # start a thread for receiving in parallel
t1.start()
while True: # start taking input to send
    msg  = raw_input()
    s.sendall(msg.encode())
