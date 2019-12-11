import socket # for socket 
import argparse
import pickle
import sys

# take IP & port as command line argument
parser = argparse.ArgumentParser()

parser.add_argument('--ip', type=str,
                    help='IP Addr')
parser.add_argument('--port', type=int,
                    help='server port')


args = parser.parse_args()

try: # create a INET socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
except socket.error as err: 
    print ("socket creation failed with error %s" %(err)) 
  
port = 80
   

s.connect((args.ip, args.port)) # connect to server
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
	elif command == 'close': #close connection
		s.close()
		sys.exit()
	else:
		print(res)