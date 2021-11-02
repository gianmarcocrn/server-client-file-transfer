import sys
import socket
import os

# Sends listing of current directory
def send_listing(socket):
	current_listing = os.listdir() 							# current directory listing in list form
	current_listing_string = ",".join(current_listing)		# joining list into string to encode it (list can't be encoded)
	socket.sendall(current_listing_string.encode("utf-8"))

# Receives listing of current directory
def recv_listing(socket):
	data = socket.recv(4096)
	decoded_string = data.decode("utf-8")
	print("Current directory: " + "\n" + decoded_string)


# Opens 'filename' file and sends its data over the network through the provided socket
# Used in client for put, in server for get
def send_file(socket,filename): 
	with open(filename, 'rb') as f: 						# open file in read binary mode
		while True:
			bytes_read = f.read(4096*8) 					# Reads bits 4096 bytes at a time
			if not bytes_read: 								# If chunk is empty break
				break
			socket.sendall(bytes_read) 


# Creates 'filename' file and stores into it data received from the provided socket
# Used in client for get, in server for put
def recv_file(socket,filename):
	with open(filename, 'wb') as f:							# opens filename in write binary mode
		while True:
			bytes_to_write = socket.recv(4096)  			# gets 4096 bytes from socket to write on file at a time
			if not bytes_to_write:							# if chunk is empty break
				break
			f.write(bytes_to_write)
