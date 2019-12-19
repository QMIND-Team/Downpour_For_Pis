import socket

def import_code(filename):
    '''Import file to list of lines.'''
    file = 'failed to read file'
    with open(filename,'r') as f:
        return f.read()
    return file

def ts(msg: str):
   s.send(msg.encode()) 
   data = ''
   data = s.recv(1024).decode()
   print (data)

def send(msg: str, ip: str):
   '''Push a string to a specified IP address.'''
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   port = 8000
   s.connect((ip, port))
   msg = msg
   s.send(msg.encode())
   # data = ''
   data = s.recv(1024).decode()
   return data

def request(type: str, ip: str):
   pass

if __name__ == '__main__':

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   host ="localhost"
   port = 8000
   s.connect((host,port))

   # filename = "DickensASCII.txt"
   # f = import_code(filename)
   # ts(f)

   while 2:
      r = input('enter: ')
      ts(r)

   s.close ()