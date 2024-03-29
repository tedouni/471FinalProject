import socket
import sys
import os


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
	# for file in localFiles:
	# 	print file
	# print len(localFiles)
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

def serverSendFile(fileName, client):
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

	try:
		fileSize = str(os.path.getsize(fileName))
		newClient.send((fileSize))
	except os.error:
		print 'ERROR: File does not exist'
		newClient.send(str(0))
		newClient.close()
		exit()

	receivedTest = newClient.recv(CLIENT_MSG_SIZE)
	if (receivedTest != fileSize):
		print 'ERROR in File Size'
		newClient.close()
		exit()
	else:
		outputFile = open(fileName, 'rb')
		bytesSent = 0


		while(bytesSent != int(fileSize)):
			tempData = outputFile.read(64)
			newClient.send(tempData)
			bytesSent += len(tempData)
	outputFile.close()
	print 'Closing Data Connection'
	newClient.close()

def getClientFile(fileName,client):
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

	fileSize = newClient.recv(CLIENT_MSG_SIZE)
	print  "fileSize = " + str(fileSize)

	inputFile = open(fileName,'wb')

	#ACK that we received fileSize
	newClient.send(fileSize)
	bytesRecvd = 0

	while(bytesRecvd != int(fileSize)):
	    tempData = newClient.recv(CLIENT_MSG_SIZE)
	    # print tempData
	    bytesRecvd += len(tempData)

	    if not tempData:
	        break
	    inputFile.write(tempData)
	print 'Recieved ' + str(bytesRecvd) + ' bytes out of ' +str(fileSize) + ' bytes'
	print 'Closing Data Connection'
	inputFile.close()
	newClient.close()
	print 'Data Connection closed'
	print '\n'


def main():
	port = int(sys.argv[1])

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
		print "GOT: '" + str(data) + "' from client"

		if(data == "quit"):
			print "Closing Connection"
			client.close()
			print "Connection Closed"
			break
		elif (data == "ls"):
			localList(client)
		elif (data[:3] == 'get'):
			serverSendFile(data[4:],client)
		elif (data[:3] == 'put'):
			getClientFile(data[4:],client)
		else:
			pass

		# client.send("DONE")

if __name__ == '__main__':
	main()
