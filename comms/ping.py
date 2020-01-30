#importing socket module 
import socket 
  
#creates a new socket using the given address family. 
socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
#setting up the default timeout in seconds for new socket object 
socket.setdefaulttimeout(1) 
  
#returns 0 if connection succeeds else raises error 
addr = socket.gethostbyname(socket.gethostname())
port = 12345
result = socket_obj.connect_ex((addr,port)) #address and port in the tuple format 
  
#closes te object 
socket_obj.close() 