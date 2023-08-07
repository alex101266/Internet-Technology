from TCP_socket_p2 import TCP_Connection
import time

class TCP_Connection_Final(TCP_Connection):
	"""docstring for TCP_Connection_Final"""
	def __init__(self, self_address, dst_address, self_seq_num, dst_seq_num, log_file=None):
		super().__init__(self_address, dst_address, self_seq_num, dst_seq_num, log_file)
	def handle_timeout(self):
		#put code to handle RTO timeout here
		#send a single packet containing the oldest unacknowledged data
		#increase the RTO timer 
		pass
	def handle_window_timeout(self):
		#put code to handle window timeout here
		#in other words, if we haven't sent any data in while (which causes this time to go off),
		#send an empty packet
		pass
	def receive_packets(self, packets):
		#insert code to deal with a list of incoming packets here
		#NOTE: this code can send one packet, but should never send more than one packet
		pass
	def send_data(self, window_timeout = False, RTO_timeout = False):
		#put code to send a single packet of data here
		#note that this code does not always need to send data, only if TCP policy thinks it makes sense
		#if there is any data to send, i.e. we have data we have not sent and we are allowed to send by our
		#congestion and flow control windows, then send one packet of that data

		#Check how much data can be sent
		size = min(self.SND.MSS, self.SND.WND, self.congestion_window)
		start = self.SND.NXT - self.SND.UNA
		end = start + size

		#Get the needed segment from send_buff
		segment = self.send_buff[start:end]
		#print("*****",start,size,end,segment)

		#Check push flag, send one packet
		flag = False
		data_to_send = bytearray()
		for byte in segment:
			if not isinstance(byte,int) and byte.endswith(b'PSH'):
				flag = True
				byte = byte[0]
			data_to_send.append(byte)

		#Sends data (if there is any)
		if data_to_send:
			self._packetize_and_send(self.SND.NXT, PSH=flag, data = data_to_send)
			self.SND.NXT += len(data_to_send)