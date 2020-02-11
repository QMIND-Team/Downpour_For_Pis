"""Transport module for receiving data from workers."""

import socket
import json # Just for debugging

class Server():
    def __init__(self, response_policy: object):
        """Server Constructor"""
        self.manager_ip = 'localhost'
        self.port = 12346
        self.response_policy = response_policy

    def recv_fromWorker(self, conn: socket):
        """Receive string from Worker via the client module."""
        msg = []
        conn.settimeout(0.2) # is there a better way to do this???
        while True: # receive data 1024 bytes at a time
            try:
                data = conn.recv(32)
            except:
                break
            msg.append(data) # append decoded string

        message = b''.join(msg).decode(encoding='UTF-32') # concatenate string

        return message

    def run(self):
        """Describes the workflow of the Manager."""

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.manager_ip, self.port))
        s.listen(5)
        print('Server listening...')

        while True:
            # receive
            conn, addr = s.accept()
            print("got something")
            msg = self.recv_fromWorker(conn)
            print(str(addr[0]) + " sent "+ json.loads(msg)['type'])

            # respond
            # Duncan - I'm worried that if no message is recieved, msg will be None and it might cause response_policy to fuck up 
            # putting this in an if(msg != None): block might be a good idea
            response = self.response_policy(msg)
            conn.send(response.encode(encoding='UTF-32'))

            # close
            conn.close()
