"""Transport module for receiving data from workers."""

import socket
import json     # For debugging only

if __name__ == "__main__":
    from config import MANAGER_IP
else:
    from comms.config import MANAGER_IP

class Server():
    def __init__(self, model, response_policy):
        """Server Constructor"""
        self.manager_ip = MANAGER_IP
        self.host = socket.gethostname() # Get local machine name
        self.port = 12345
        self.response_policy = response_policy
        self.model = model

    def recv_from_worker(self, conn):
        """Receive string from Worker via the client module."""
        
        length = int.from_bytes(conn.recv(4), 'big')
        chunks = []
        total_received = 0
        while total_received < length:
            chunk = conn.recv(min(length - total_received, 2048))
            total_received += len(chunk)
        
        message = b''.join(chunks)
        return message.decode(encoding='UTF-8')

    def run(self):
        """Describes the workflow of the Manager."""

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        print('Server listening...')

        while True:
            # receive
            conn, addr = s.accept()
            msg = self.recv_from_worker(conn)
            print(f"{str(addr[0])} sent {json.loads(msg)['type']} message")

            # respond
            response = self.response_policy(self.model, msg)
            conn.send(response.encode(encoding='UTF-8'))    # TODO FIX

            # close
            conn.close()
