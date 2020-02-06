"""Transport module for receiving data from Workers"""

from json import loads, dumps
import socket
from messages import Init, Init_Response, Fetch, Fetch_Response, Push, Terminate, Message

class Server():
      def __init__(self, response_policy: object):
            """response_policy is a method describing how to reply to different message types."""
            manager_ip = "192.168.0.100" # TODO Replace this with reading manager's ip from config file
            self.manager_ip = manager_ip
            self.host = socket.gethostname() # Get local machine name
            self.port = 12345
            self.response_policy = response_policy # used Noun naming because it is treated like a Noun here

      def recv_fromWorker(self, conn: socket):
            """Receive string from Worker via the client module."""
            
            msg = []
            while True: # receive data 1024 bytes at a time
                  data = conn.recv(1024)
                  if data: print('Receiving data...')
                  if not data: break
                  msg.append(data.decode(encoding='UTF-8')) # append decoded string

            msg = ''.join(msg)
            return loads(msg)

      def run(self):
            """Describes the workflow of the Manager."""

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = socket.gethostname()
            port = 12345                
            s.bind((host, port))
            s.listen(5)
            print('Server listening...')
            
            while True:  
                  # receive
                  conn, addr = s.accept()
                  msg = self.recv_fromWorker(conn)
                  print(str(addr[0]) + " sent a "+ msg["type"] +" message")

                  # respond
                  response = self.response_policy(msg)
                  conn.send(response)

                  # close
                  conn.close()

