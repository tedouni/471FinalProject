import socket
import sys
import os


def localList(client):
	#Setup ephemeral
	newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	newSock.bind(('',0))
	newSock.listen(backlog)

	#send port number to client
	sendPortNum = newSock.getsockname()[1]
	client.send(str(sendPortNum))
	print "Connecting on port " + sendPortNum
	newClient , newAddress = newSock.accept()
	print "Connected on port " +sendPortNum

	localFiles = os.listdir(".")
	newClient.send(str(len(localFiles)))





port = 1200
backlog = 100
# Create A TCP socket
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bing the socket to the port
listenSocket.bind(('',port))

# Start listening for incoming connectionsx
listenSocket.listen(backlog)

# The client message size
CLIENT_MSG_SIZE = 1024
print "Listening on port %d" % listenSocket.getsockname()[1]
# Service clients forever

while 1:

	# Accept a connection from the client
	client, address = listenSocket.accept()

	# Get the data from the client
	data = client.recv(CLIENT_MSG_SIZE)
	print "GOT: " + str(data) + " from client"

	if(data == "quit"):
		print "Closing Connection"
		client.close()
		print "Connection Closed"
		break
	elif (data == "ls"):
		localList(client)

	client.send("DONE")

	# Close the connection to the client
