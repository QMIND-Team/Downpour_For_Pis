"""Transport module for receiving data from workers."""

import json     # For debugging only
import socket

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
