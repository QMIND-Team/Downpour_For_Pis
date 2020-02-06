"""Transport module for sending strings to the manager."""

import json
import socket

class Client():
      def __init__(self):
            manager_ip = "192.168.0.100" # TODO Replace this with reading manager's ip from config file
            self.manager_ip = manager_ip
            self.host = socket.gethostname() # Get local machine name
            self.port = 12345

      def send(self, data: str):
            """Send string to Manager via the server module. Works differently than Server.send()"""
            
            srvr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srvr.connect((self.host, self.port)) 

            if data[-4:] == ".txt":
                  with open(data, 'rb') as f:
                        print('File opened.')
                        data = f.read(1024)
                        while (data):
                              srvr.send(data)
                              data = f.read(1024)

                        print('Sent text file as string.')
                        f.close()
            else:
                  srvr.send(data.encode(encoding='UTF-8'))
                  print('Sent string.')

            response = "" # do this

            srvr.close()                     # Close the socket when done

            return response
