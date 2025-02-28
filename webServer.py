# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
  
    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)  # Enable the server to accept connections
    
    print(f"Server is listening on port {port}")

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Accept the connection from a client
        
        try:
            message = connectionSocket.recv(1024).decode()  # A client is sending you a message
            filename = message.split()[1]
            
            # Open the client requested file.
            # Make sure to handle the case where the file might not exist.
            f = open(filename[1:], "rb")  # Opening the requested file in binary mode
            
            # This variable can store the headers you want to send for any valid or invalid request.
            # Send a header for a valid request (200 OK)
            outputdata = b"HTTP/1.1 200 OK\r\n"  # Standard 200 OK response header
            outputdata += b"Content-Type: text/html; charset=UTF-8\r\n"
            outputdata += b"\r\n"  # Blank line to end the headers
            
            # Send the header first, then the content of the requested file.
            connectionSocket.sendall(outputdata)  # Send headers
            for i in f:  # for each byte in the file
                connectionSocket.sendall(i)  # Send file contents

            f.close()  # Close the file after sending the content

            connectionSocket.close()  # Closing the connection socket
        
        except Exception as e:
            # Send response message for invalid request due to the file not being found (404)
            # Send a 404 Not Found response
            outputdata = b"HTTP/1.1 404 Not Found\r\n"
            outputdata += b"Content-Type: text/html; charset=UTF-8\r\n"
            outputdata += b"\r\n"
            outputdata += b"<html><body><h1>404 Not Found</h1></body></html>"
            
            connectionSocket.sendall(outputdata)  # Send 404 response

            # Close client socket
            connectionSocket.close()

    # Commenting out the below (some use it for local testing). It is not required for Gradescope, and some students have moved it erroneously in the While loop. 
    # DO NOT PLACE ANYWHERE ELSE AND DO NOT UNCOMMENT WHEN SUBMITTING, YOU ARE GONNA HAVE A BAD TIME
    # serverSocket.close()
    # sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":
    webServer(13331)
