import socket
import sys
import os
#test
port = 1200
backlog = 100
# The client message size
CLIENT_MSG_SIZE = 1024
def localList(client):
	#Setup ephemeral
	print "Setting up Data Connection"
	newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	newSock.bind(('',0))
	newSock.listen(backlog)

	#send port number to client
	sendPortNum = newSock.getsockname()[1]
	client.send(str(sendPortNum))
	print "Connecting on port " + str(sendPortNum)
	newClient , newAddress = newSock.accept()
	print "Connected on port " + str(sendPortNum)


	localFiles = os.listdir(".")
	for file in localFiles:
		print file
	print len(localFiles)
	#Send current item
	newClient.send(str(len(localFiles)))


	recieveCheck =newClient.recv(CLIENT_MSG_SIZE)

	if int(recieveCheck) != len(localFiles):
		print "ERROR in transmission of # of files"
		newClient.close()
		exit()
	else:
		for file in localFiles:
			if not file:
				pass
			else:
				newClient.send(file)
				recieveCheck = newClient.recv(CLIENT_MSG_SIZE)
				if(recieveCheck != file):
					print 'ERROR in transmiting fileName'
					print 'Resending'
					newClient.send(file)



	print "Closing Data Connection"
	newSock.close()
	print "Data Connection Closed"






def main():


	# Create A TCP socket
	listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the port
	listenSocket.bind(('',port))

	# Start listening for incoming connectionsx
	listenSocket.listen(backlog)


	# Service clients forever
	client, address = listenSocket.accept()
	while 1:

		# Accept a connection from the client
		print "Listening on port %d" % listenSocket.getsockname()[1]


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
		else:
			pass

		# client.send("DONE")

if __name__ == '__main__':
	main()
