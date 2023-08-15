from sys import argv
import socket
import argparse
import time

# Parse command line arguments
parser=argparse.ArgumentParser(description="""This is an SMTP sender""")
parser.add_argument('email_file', type=str, help='this is the filename of the email body',action='store')
parser.add_argument('subject_line', type=str, help='this is the email\'s subject line, remeber to include " " around the subject',action='store')
parser.add_argument('destination_email_address', type=str, help='This is the destination email address, includes only gmail addresses for now',action='store')
parser.add_argument('source_username', type=str, help='This is the username of the source email the end is implied to be the current machine',action='store')
parser.add_argument('-s', type=str, dest='dest_serv', help='This is the destination SMTP server, defaults to gmails',action='store', default='gmail-smtp-in.l.google.com.')
args = parser.parse_args(argv[1:])

# Connect to the SMTP server
out_sock = socket.socket()
out_sock.connect((args.dest_serv,25))

# Receive and display the server's greeting
recv_data = out_sock.recv(1024).decode()
# print(f"From Server: {recv_data}")

# Send the HELO command
out_sock.send(b"HELO " + socket.gethostname().encode() + b"\r\n")
recv_data = out_sock.recv(1024).decode()
print(f"To Server: {'HELO ' + socket.gethostname()}\nFrom Server: {recv_data}")

# Send the MAIL FROM command (ERROR, INVALID RFC SENDER ADDRESS)
#out_sock.send(b"MAIL FROM:<" + args.source_username.encode() + b">\r\n")
#recv_data = out_sock.recv(1024).decode()
#print(f"To Server: {'MAIL FROM:<' + args.source_username + '>'}\nFrom Server: {recv_data}")

# Send the MAIL FROM command (ERROR, SYNTAX)
#out_sock.send(b"MAIL FROM:<" + {args.source_username}@{socket.gethostname()} + b">\r\n")
#recv_data = out_sock.recv(1024).decode()
#print(f"To Server: {'MAIL FROM:<' + {args.source_username}@{socket.gethostname()} + '>'}\nFrom Server: {recv_data}")

# Send the MAIL FROM command
out_sock.send(b"MAIL FROM:<" + f"{args.source_username}@{socket.gethostname()}".encode() + b">\r\n")
recv_data = out_sock.recv(1024).decode()
print(f"To Server: {'MAIL FROM:<' + args.source_username + '@' + socket.gethostname() + '>'}\nFrom Server: {recv_data}")


# Send the RCPT TO command
out_sock.send(b"RCPT TO:<" + args.destination_email_address.encode() + b">\r\n")
recv_data = out_sock.recv(1024).decode()
# print(f"To Server: {'RCPT TO:<' + args.destination_email_address + '>'}\nFrom Server: {recv_data}")

# Send the DATA command
out_sock.send(b"DATA\r\n")
recv_data = out_sock.recv(1024).decode()
# print(f"To Server: {'DATA'}\nFrom Server: {recv_data}")

# Construct the Message-ID header
message_id = f"<{int(time.time())}@{socket.gethostname()}>"

# Construct the email message
email_subject = f"Subject: {args.subject_line}\r\n"
email_from = f"From: <{args.source_username}@{socket.gethostname()}>\r\n"
email_message_id = f"Message-ID: {message_id}\r\n"
email_to = f"To: <{args.destination_email_address}>\r\n"
email_headers = email_from + email_to + email_subject + email_message_id

with open(args.email_file, 'r') as email_file:
    email_body = email_file.read()

email_data = email_headers + "\r\n" + email_body + "\r\n.\r\n"
out_sock.send(email_data.encode())
recv_data = out_sock.recv(1024).decode()
# print(f"To Server:\n{email_data}\nFrom Server: {recv_data}")

# Send the QUIT command
out_sock.send(b"QUIT\r\n")
recv_data = out_sock.recv(1024).decode()
# print(f"To Server: QUIT\nFrom Server: {recv_data}")

# Close the socket
out_sock.close()

# print("Email sent successfully!")
