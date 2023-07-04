import socket
from sys import argv
import argparse


#Used the parser from the provided Client.py, with a minor adjustment
parser=argparse.ArgumentParser(description="""This is the corresponding server program""")
#parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='source_strings.txt',action='store', dest='in_file')
#parser.add_argument('-o', type=str, help='This is the destination file for the reversed strings', default='results.txt',action='store', dest='out_file')
parser.add_argument('port', type=int, help='This is the port to bind the server on',action='store')
args = parser.parse_args()
print(args.port)
#Creates the server socket.
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Binds the server socket to indicated port and sets the server location to an empty string, 
# which lets it listen for all networks rather than just a specific ip or local host.
server_addr = (socket.gethostname(), args.port)
print(server_addr)
server_sock.bind(server_addr)

#Listens for incoming connections from the client computer.
server_sock.listen(5)

while True:
    print("Waiting to connect...")

    #Client is found and connected to.
    client_sock, client_addr = server_sock.accept()
    print("Connected to: ", client_addr)

    while True:
        #reads data
        data = client_sock.recv(512)
        #breaks if end of file
        if not data:
            break
        modified_data = data.decode("utf-8").swapcase()
        #sends reversed case to client
        client_sock.send(bytes(modified_data,'utf-8'))
    #Closes the client once finished transferring data.
    client_sock.close()

    #Closes the server socket after client is finished sending strings and also closed.
    break