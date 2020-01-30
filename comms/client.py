"""Transport module for sending strings to the manager."""

import socket               # Import socket module

def send_toManager(data: str, srvr: socket):
      """Send string to Manager via the server module."""
      
      if data[-4:] == ".txt":
            with open(data, 'rb') as f:
                  print('File opened.')
                  data = f.read(1024)
                  while (data):
                        srvr.send(data)
                        data = f.read(1024)

                  print('Sent text file as string.')
                  f.close()
            
      else:
            srvr.send(data)
            print('Sent string.')
            
      

def main():
      """This is a script a Worker would run."""

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      host = socket.gethostname() # Get local machine name
      port = 12345                # used in local transport protocol

      s.connect((host, port)) 

      # if sending a string directly, make sure it doesn't end
      # with the .txt extenion!!!
      path_or_string = 'small_file.txt'

      send_toManager(path_or_string, s)

      print('Done sending')
      
      s.close()                     # Close the socket when done

if __name__ == "__main__":
      main()
   