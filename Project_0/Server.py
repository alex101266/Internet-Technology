import socket
import argparse

#Used the parser from the provided Client.py, with a minor adjustment
parser=argparse.ArgumentParser(description="""This is the corresponding server program""")
parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='source_strings.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination file for the reversed strings', default='results.txt',action='store', dest='out_file')
parser.add_argument('port', type=int, help='This is the port to bind the server on',action='store')
args = parser.parse_args()

#Creates the server socket.
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Binds the server socket to indicated port and sets the server location to an empty string, 
# which lets it listen for all networks rather than just a specific ip or local host.
server_addr = ('', args.port)
server_sock.bind(server_addr)

#Listens for incoming connections from the client computer.
server_sock.listen(1)

#A function for repeatedly switching lowercase to uppercase and vice versa for each string sent from client.
def switched_string(input_string):
    switched_string = input_string.swapcase()
    return switched_string

while True:
    print("Waiting to connect...")

    #Client is found and connected to.
    client_sock, client_addr = server_sock.accept()
    print("Connected to: ", client_addr)

    #Opens the original and result files.
    with open (args.out_file, 'wb') as write_file:
        for line in open(args.in_file, 'rb'):
            #This is the data received from client.
            data = client_sock.recv(512)

            if not data:
                break

            #Switches the strings.
            switched_data = switched_string(data.decode())
            write_file.write(switched_data.encode() + b'\n')

            #Sends the switched data back to client.
            client_sock.sendall(switched_data.encode())

    #Closes the client once finished transferring data.
    client_sock.close()

    #Closes the server socket after client is finished sending strings and also closed.
    break