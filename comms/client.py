"""Transport module for sending strings to the manager."""

import socket               # Import socket module

class Client():
      def __init__(self):
            manager_ip = "192.168.0.100" # TODO Replace this with reading manager's ip from config file
            self.manager_ip = manager_ip
            self.host = socket.gethostname() # Get local machine name
            self.port = 12345

      def send(self, data: str):
            """Send string to Manager via the server module."""
            
            srvr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srvr.connect((self.host, self.port)) 


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
                  srvr.send(data.encode(encoding='UTF-8'))
                  print('Sent string.')

            # response = srvr.read()
            
            srvr.close()                     # Close the socket when done

            tmp = ""
            return tmp
                  
      

def main():
      """This is a script a Worker would run."""

      client = Client()

      # if sending a string directly, make sure it doesn't end
      # with the .txt extenion!!!
      path_or_string = 'small_file.txt'

      response = client.send(path_or_string)
      print(response)
      print('Done sending')
      

if __name__ == "__main__":
      main()
   