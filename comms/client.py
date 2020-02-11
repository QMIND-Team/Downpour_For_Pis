"""Transport module for sending strings to the manager."""

import socket

class Client():
    def __init__(self):
        self.manager_ip = 'localhost'
        self.port = 12346

    def send(self, msg: str):
        """Send string to Manager via the server module. Works differently than Server.send()"""
        
        srvr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srvr.connect((self.manager_ip, self.port))
        
        srvr.send(msg.encode(encoding='UTF-32'))
        print('Sent message.')

        resp = []
        srvr.settimeout(20.0) # is there a better way to do this???
        while True: # receive data 1024 bytes at a time
            data = srvr.recv(16)
            print(data)
            if data == b'':
                break
            print(data.decode(encoding='UTF-32'))
            resp.append(data) # append decoded string

        if resp is None: # shut down and retry
            srvr.close()
            return None

        response = b''.join(resp).decode(encoding='UTF-32')

        srvr.close()                     # Close the socket when done

        return response
