import socket                
import argparse
import threading
import os

# handles one interface ipv4/ipv6
def handle(s):
   s.listen(5)               

   while True:
      c, addr = s.accept()  # start accepting connections
      print ('Handling client ', addr)
      c.send('Enter your command please'.encode())
      while(True):
         command = c.recv(4096).decode() # receive command
         command = command.split(' ')
         if command[0] == 'download':
            try:
               f = open(command[1],'rb') # open file and send its content to client
               data = f.read(4096)
               c.sendall(data.encode())
               f.close()
            except:
               c.sendall('Problem in opening file'.encode())
         elif command[0] == 'run':
            stream = os.popen(' '.join(command[1:])) # execute a shell comand and send its output
            output = stream.read()
            c.sendall(output.encode())
         elif command[0] == 'close': # close connection
            c.send('Closing...'.encode())
            print('Socket Closed')
            break
         else:
            c.sendall("Command not found".encode())

# take port as command line argument
parser = argparse.ArgumentParser()

parser.add_argument('--port', type=int,
                    help='listening port')

args = parser.parse_args()

# socket to accept ipv6 connections
s1 = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)                     
s1.bind(('::1', args.port))

# socket to accept ipv4 connections
s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)                      
s2.bind(('', args.port))         

# spawn two threads for each
print ("Socket successfully created")   
t1=threading.Thread(target=handle,args=(s1,))
t2=threading.Thread(target=handle,args=(s2,))

t1.start()
t2.start()

