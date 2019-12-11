import socket # for socket 
import argparse
import sys
import ipaddress

# take IP & port as command line argument
parser = argparse.ArgumentParser()

parser.add_argument('--ip', type=str,
                    help='IP Addr')
parser.add_argument('--port', type=int,
                    help='server port')


args = parser.parse_args()
sock_family = socket.getaddrinfo(args.ip,args.port)[0][0]
if sock_family == socket.AF_INET6: # create a INET6 socket
	s =  socket.socket (socket.AF_INET6, socket.SOCK_STREAM)
	s.connect((args.ip, args.port)) # connect to server
else: # create a INET socket
	s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	s.connect( (args.ip, args.port) ) # connect to server

msg = s.recv(4096)
print(msg.decode())

while True:
	command  = raw_input() # take input command and send to server
	s.sendall(command.encode())

	res = s.recv(4096).decode()
	if 'download' in command: # write in file
		fname = command.split(' ')[1] 
		f = open('client_{}'.format(fname),'w')
		f.write(res)
		f.close()
	elif command == 'close': # close connection
		s.close()
		sys.exit()
	else:
		print(res)