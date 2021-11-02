import socket
import sys
import os

sys.path.append('../')																				# go to parent folder to access sharedMod

from sharedMod import send_file,recv_file,send_listing,recv_listing

cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)										# AF_INET: address family, SOCK_STREAM:socket type
srv_addr = (sys.argv[1], int(sys.argv[2]))								
srv_addr_str = str(srv_addr)
try:
	cli_sock.connect(srv_addr)																		# connects cli_sock to server binding socket to a port on our side
except Exception as e:
	print(e)
	exit(1)

try:
	if (len(sys.argv) == 4): 																		# checking if command has 4 arguments (either 4 or 5 is possible)
		if (sys.argv[3] == "list"):
			cli_sock.sendall(sys.argv[3].encode("utf-8")) 											# send 'list' keyword over to server to trigger listing
			recv_listing(cli_sock)																	# receive directory listing
			print(sys.argv[3] + " request successfully sent to server with IP: " + srv_addr[0] + " and port #" + sys.argv[2])
		else:
			raise ValueError("Incorrect command keyword while trying a " + sys.argv[3] + "request on server with IP: " + srv_addr[0] + ", please try again")
	elif (len(sys.argv) == 5): 																		# checking if command has 5 arguments (either 4 or 5 is possible)
		if (sys.argv[3] == "get"):
			cli_sock.sendall((sys.argv[3]+" "+sys.argv[4]).encode("utf-8")) 						# send 'get' keyword and file name to trigger server 
			print(sys.argv[3] + " request on " + sys.argv[4] + " successfully sent to server with IP: " + srv_addr[0] + " and port #" + sys.argv[2])
			if (sys.argv[4] in os.listdir()):														# checking if file is already in client directory (exclusive creation)
				("Server IP: " + srv_addr[0] + " and port #" + sys.argv[1] + ". Failed " + sys.argv[3] + " request on " + sys.argv[4] + ". File already in client directory")
			else:
				recv_file(cli_sock,sys.argv[4]) 													# checking if command has 4 arguments (either 4 or 5 is possible)
		elif (sys.argv[3] == "put"):
			cli_sock.sendall((sys.argv[3]+" "+sys.argv[4]).encode("utf-8")) 						# send 'put' keyword and file name to trigger server
			send_file(cli_sock,sys.argv[4]) 
		else:
			raise ValueError("Incorrect command keyword while trying a " + sys.argv[3] + "request on server with IP: " + srv_addr[0] + ", please try again")
	else:
		raise ValueError("Incorrect command, please try again")
except Exception as e:																				# handling connection drops
	print(e,end=", ")																				
	print(sys.argv[3] + " request has failed")														# reporting failure when connection drops
	exit(1)
finally:
	cli_sock.close()																				# close client socket

exit(0) 																							# Exit with a zero value, to indicate success