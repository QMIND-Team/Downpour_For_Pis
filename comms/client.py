"""Transport module for sending strings to the manager."""

import socket

if __name__ == "__main__":
    from config import MANAGER_IP
    from config import PORT
    from socket_helper import mysend, myrecv
else:
    from comms.socket_helper import mysend, myrecv
    from comms.config import MANAGER_IP
    from comms.config import PORT

class Client():
    def __init__(self):
        """Client Constructor"""
        self.manager_ip = MANAGER_IP
        self.host = socket.gethostname() # Get local machine name
        self.port = PORT

    def send(self, message: str):
        """Send string to Manager via the server module"""
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))

        msg = message.encode(encoding='UTF-8')

        mysend(conn, msg)
        
        resp = myrecv(conn)
        response = resp.decode(encoding='UTF-8')

        # if resp is None: # shut down and retry
        #       conn.close()
        #       return None

        conn.close()

        return response
