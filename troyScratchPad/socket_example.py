"""
Following <https://www.instructables.com/id/Netcat-in-Python/>
"""

import sys
import socket
import time

def netcat(host, port, content):
    """
    Simple for now
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        sock.sendall(content)
        time.sleep(0.5)
        sock.shutdown(socket.SHUT_WR)

        res = ""

        while True:
            data = sock.recv(1024)
            if not data:
                break
            res += data.decode()

        print(res)

        print("Connection closed.")
        sock.close()

if __name__ == "__main__":
    # I won't bother with checking these correctly yet
    host = sys.argv[1]
    port = int(sys.argv[2])

    content = "GET / HTTP/1.1\nHOST: google.com\n\n"

    netcat(host, port, content.encode())
