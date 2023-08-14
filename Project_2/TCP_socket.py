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
		print('timeout')
		self.send_data(self,window_timeout=False,RTO_timeout=True)
		self.RTO_timer.set_and_start(self, self.RTO_timer.timer_length*2)
		pass
	def handle_window_timeout(self):
		print('window timeout')
		#put code to handle window timeout here
		#in other words, if we haven't sent any data in while (which causes this time to go off),
		#send an empty packet
		self.send_data(self,window_timeout=True,RTO_timeout=False)
		self.window_timer.set_and_start(self, self.window_timer.timer_length*2)
		pass
	def receive_packets(self, packets):
		#insert code to deal with a list of incoming packets here
		#NOTE: this code can send one packet, but should never send more than one packet
		for packet in packets:
			#Check sequence number
			#Send ACK if new data receieved
			if packet.LEN == 0 & self.RCV.WND == 0:
				if packet.SEQ == self.RCV.NXT:
					print('packet acknowledged')
			elif packet.LEN == 0 & self.RCV.WND >= 0:
				if self.RCV.NXT <= packet.SEQ < self.RCV.NXT + self.RCV.WND:
					print('packet acknowledged')
			elif packet.LEN >= 0 & self.RCV.WND == 0:
				#not acceptable
				print('oh nos')
			elif packet.LEN >= 0 & self.RCV.WND >= 0:
				if self.RCV.NXT <= packet.SEQ < self.RCV.NXT + self.RCV.WND:
					if packet.SEQ + packet.LEN - 1 < self.RCV.NXT + self.RCV.WND:
						self.receive_buffer[packet.SEQ-self.RCV.NXT:packet.SEQ + packet.LEN-self.RCV]=packet.data
					else:
						self.receive_buffer[packet.SEQ-self.RCV.NXT:]=packet.data[:self.RCV.WND]
				elif self.RCV.NXT <= packet.SEQ + packet.LEN - 1< self.RCV.NXT + self.RCV.WND:
					self.receive_buffer[:packet.SEQ + packet.LEN-self.RCV.NXT] = packet.data[self.RCV.NXT-packet.SEQ:]
			"""
			segment_len = packet.LEN
			if segment_len > 0:
				self.RCV.ACK = packet.SEQ + segment_len
				self.RCV.WND -= segment_len
				self._packetize_and_send(self.SND.NXT)
			"""
		
	
	def send_data(self, window_timeout = False, RTO_timeout = False):
		#put code to send a single packet of data here
		#note that this code does not always need to send data, only if TCP policy thinks it makes sense
		#if there is any data to send, i.e. we have data we have not sent and we are allowed to send by our
		#congestion and flow control windows, then send one packet of that data

		if RTO_timeout == True:
			self.SND.NXT = self.SND.UNA
		#Check how much data can be sent
		size = min(self.SND.MSS, self.SND.WND, self.congestion_window)
		if window_timeout == True:
			size = 0
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

		#Sends data (if there is any) or if zero window probing
		if data_to_send or window_timeout == True:
			self._packetize_and_send(self.SND.NXT, PSH=flag, data = data_to_send)
			self.SND.NXT += len(data_to_send)