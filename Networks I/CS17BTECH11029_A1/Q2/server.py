import socket                
import argparse
import os
import threading
uname_to_sock = {} # ductionary for mapping username to socket

def handle(uname,c):
   while True:
      msg = c.recv(4096).decode()
      if msg == 'close': # delete username if it closes connection
         c.send('Closing..'.encode())
         del uname_to_sock[uname]
         return
      msg = msg.split('|') # decode message and send it to receiver
      dmsg = [uname,'|',msg[0]]
      dmsg = ' '.join(dmsg)
      if msg[1] in uname_to_sock:
         uname_to_sock[msg[1]].sendall(dmsg.encode())
      else:
         c.send('Server | Receiver not online'.encode())

parser = argparse.ArgumentParser()

# listening port
parser.add_argument('--port', type=int,
                    help='listening port')

args = parser.parse_args()

s = socket.socket()          
print ("Socket successfully created")

port = args.port               

s.bind(('', port))         

s.listen(5)               

while True: 

   c, addr = s.accept() # accept connections
   uname = c.recv(4096).decode()
   print ('Handling client ', uname)   
   c.send('Message please') 
   uname_to_sock[uname] = c # add username to dict
   t1=threading.Thread(target=handle,args=(uname,c)) # launch the thread
   t1.start()
