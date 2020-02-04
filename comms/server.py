"""Transport module for receiving data from Workers"""

import socket

def recv_fromWorker(conn: socket):
    """Receive string from Worker via the client module."""
    
    msg = []

    while True:
        data = conn.recv(1024)
        if data: print('Receiving data...') # may need to stitch messages together
        if not data: break # if no more bits received
        msg.append(data.decode(encoding='UTF-8')) # append decoded string

    # confirm response?
    # conn.send('Thank you for connecting'.encode(encoding='UTF-8'))

    conn.close()                # Close the connection
    return ''.join(msg)

def main():
    """This is a script that a Manager would run."""
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345                
    s.bind((host, port))
    s.listen(5)
    print('Server listening...')

    while True:
        
        conn, addr = s.accept()     # Establish connection with client <3
        print('Got connection from: ' + str(addr[0]))
        message = recv_fromWorker(conn) # receive string from socket connection
        print(message)

if __name__ == '__main__':
    main()
