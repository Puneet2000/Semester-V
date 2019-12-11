import socket                
import argparse
import os

# take port as command line argument
parser = argparse.ArgumentParser()

parser.add_argument('--port', type=int,
                    help='listening port')

args = parser.parse_args()

s = socket.socket() # create a INET socket
print ("Socket successfully created")
port = args.port
s.bind(('', port)) # run on local host 127.0.0.1
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
            f = open(command[1],'rb')  # open file and send its content to client
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
