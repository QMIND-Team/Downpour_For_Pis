"""Transport module for receiving data from workers."""

import socket
if __name__ == "__main__":
      from config import MANAGER_IP
else:
      from comms.config import MANAGER_IP

class Server():
    def __init__(self, response_policy: object):
        """response_policy is a method describing how to reply to different message types."""
        self.manager_ip = MANAGER_IP
        self.host = socket.gethostname() # Get local machine name
        self.port = 12345
        self.response_policy = response_policy # used Noun naming because it is treated like a Noun here

    def recv_fromWorker(self, conn: socket):
        """Receive string from Worker via the client module."""
        
        msg = []
        conn.settimeout(0.2) # is there a better way to do this???
        while True: # receive data 1024 bytes at a time
            try:
                data = conn.recv(1024)
            except:
                break
            msg.append(data.decode(encoding='UTF-8')) # append decoded string

        message = ''.join(msg) # concatenate string

        return message

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
            print(str(addr[0]) + " sent "+ msg)

            # respond
            # Duncan - I'm worried that if no message is recieved, msg will be None and it might cause response_policy to fuck up 
            # putting this in an if(msg != None): block might be a good idea
            response = self.response_policy(msg)
            conn.send(response.encode(encoding='UTF-8'))

            # close
            conn.close()
