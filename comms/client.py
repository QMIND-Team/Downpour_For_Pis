"""Transport module for sending strings to the manager."""

from json import loads, dumps
import socket
from messages import Init_Response, Fetch_Response, Terminate

class Client():
      def __init__(self):
            manager_ip = "192.168.0.100" # TODO Replace this with reading manager's ip from config file
            self.manager_ip = manager_ip
            self.host = socket.gethostname() # Get local machine name
            self.port = 12345

      def send(self, msg: str):
            """Send string to Manager via the server module. Works differently than Server.send()"""
            
            srvr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srvr.connect((self.host, self.port)) 

            msg = dumps(msg.__dict__)

            srvr.send(msg.encode(encoding='UTF-8'))
            print('Sent message.')

            resp = []
            srvr.settimeout(5.0) # is there a better way to do this???
            while True: # receive data 1024 bytes at a time
                  data = srvr.recv(1024).decode(encoding='UTF-8')
                  if data == '': break
                  resp.append(data) # append decoded string
            
            if resp is None: # shut down and retry
                  srvr.close()
                  return None

            resp_dict = loads(''.join(resp)) # concatenate string and load JSON to dict

            if resp_dict["type"] == "init_resp":
                  response = Init_Response(resp_dict)
            elif resp_dict["type"] == "fetch_resp":
                  response = Fetch_Response(resp_dict)
            elif resp_dict["type"] == "terminate":
                  response = Terminate(resp_dict)
            else: raise TypeError("Didn't receive a known message type")

            srvr.close()                     # Close the socket when done

            return response
