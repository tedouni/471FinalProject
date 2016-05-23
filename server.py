import socket
port = 1200

backlog = 100
# Create A TCP socket
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bing the socket to the port
listenSocket.bind(('',port))

# Start listening for incoming connections
listenSocket.listen(backlog)

# The client message size
CLIENT_MSG_SIZE = 1024

# Service clients forever
while 1:

	# Accept a connection from the client
	client, address = listenSocket.accept()

	# Get the data from the client
	data = client.recv(CLIENT_MSG_SIZE)

	print "GOT: ", data, " from the client"

	client.send("DONE")

	# Close the connection to the client
	client.close()
