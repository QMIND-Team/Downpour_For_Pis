"""Transport module for receiving data from Workers"""

import json
import socket
from messages import Init, Init_Response, Fetch, Fetch_Response, Push, Terminate, Message

class Server():
      def __init__(self, response_policy: object):
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

            conn.send('hi')
            conn.close()                # Close the connection
            return ''.join(msg)

      def run(self):
            """Describes the workflow of the Manager."""
            pass
