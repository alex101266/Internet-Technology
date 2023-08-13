from sys import argv
import socket
import argparse
import time
parser=argparse.ArgumentParser(description="""This is an SMTP sender""")
parser.add_argument('email_file', type=str, help='this is the filename of the email body',action='store')
parser.add_argument('subject_line', type=str, help='this is the email\'s subject line, remeber to include " " around the subject',action='store')
parser.add_argument('destination_email_address', type=str, help='This is the destination email address, includes only gmail addresses for now',action='store')
parser.add_argument('source_username', type=str, help='This is the username of the source email the end is implied to be the current machine',action='store')
parser.add_argument('-s', type=str, dest='dest_serv', help='This is the destination SMTP server, defaults to gmails',action='store', default='gmail-smtp-in.l.google.com.')
args = parser.parse_args(argv[1:])

out_sock = socket.socket()
out_sock.connect((args.dest_serv,25))

