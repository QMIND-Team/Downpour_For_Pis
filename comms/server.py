"""Transport module for receiving data from workers."""

import tensorflow as tf
import json     # For debugging only
import socket

tf.compat.v1.logging.set_verbosity( tf.compat.v1.logging.ERROR)

if __name__ == "__main__":
    from config import MANAGER_IP
    from config import PORT
    from socket_helper import mysend, myrecv
else:
    from comms.socket_helper import mysend, myrecv
    from comms.config import MANAGER_IP
    from comms.config import PORT

class Server():
    def __init__(self, model, response_policy):
        """Server Constructor"""
        self.manager_ip = MANAGER_IP
        self.host = socket.gethostname() # Get local machine name
        self.port = PORT
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
            msg = myrecv(conn)
            message = msg.decode(encoding='UTF-8')
            print(f"{str(addr[0])} sent {json.loads(message)['type']} message")

            # respond
            response = self.response_policy(self.model, message)
            resp = response.encode(encoding='UTF-8')
            mysend(conn, resp)

            # close
            conn.close()
