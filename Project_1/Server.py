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

#Computes checksum for array of bytes
def checksum(data):
    message_sum = 0
    i = 0
    if len(data) % 2 == 1:
        data = data + b'\x00'
    while i < len(data):
        message_sum = message_sum + int.from_bytes(data[i:i+2],"big")
        message_sum = ((message_sum >> 16) + (message_sum & 0xFFFF))
        #print(message_sum)
        i += 2
    message_sum = 0xFFFF&~message_sum
    return ((message_sum).to_bytes(2,"big"))

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
        chksm = checksum(full_data)
        #makes final_data ERROR if checksum is wrong
        if chksm != b'\x00\x00':
            final_data = b'\0\0ERROR\n'
        #reverses the message and computes new checksum for final data
        else:
            modified_message = full_message.decode('ISO-8859-1').swapcase()
            modified_data = bytes(modified_message, 'ISO-8859-1')
            mod_chksm=checksum(modified_data)
            final_data = mod_chksm + modified_data
        #sends final data to client
        client_sock.send(final_data)
    #Closes the client once finished transferring data.
    client_sock.close()

    #Closes the server socket after client is finished sending strings and also closed.
    break