import socket
from sys import argv
import argparse


#Used the parser from the provided Client.py, with a minor adjustment
parser=argparse.ArgumentParser(description="""This is the corresponding server program""")
parser.add_argument('port', type=int, help='This is the port to bind the server on',action='store')
args = parser.parse_args()
#Creates the server socket.
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Binds the server socket to indicated port and sets the server location to an empty string, 
# which lets it listen for all networks rather than just a specific ip or local host.
server_addr = (socket.gethostname(), args.port)
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
        full_data = client_sock.recv(512)
        #breaks if end of file
        if not full_data:
            break
        first_two_bytes = full_data[:2]
        full_message = full_data[2:]
        message_sum = sum(full_message)
        ones_complement = ~message_sum & 0xFFFF
        ones_complement_as_bytes = ones_complement.to_bytes(2, 'big')
        modified_data = full_message.decode("utf-8").swapcase()
        final_message = modified_data + ones_complement_as_bytes
        #sends reversed case to client
        client_sock.send(bytes(final_message,'utf-8'))
    #Closes the client once finished transferring data.
    client_sock.close()

    #Closes the server socket after client is finished sending strings and also closed.
    break