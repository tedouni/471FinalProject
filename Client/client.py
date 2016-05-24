import socket
import sys
import os

SERVER_MSG_SIZE = 1024
def clientLocalListing():
    print "Listing files on client:"
    directoryListing = os.listdir(".")
    for file in directoryListing:
        print file
    print "\n"
def displayCommands():
        print "Choose from the following selections:"
        print "ftp> get <filename> (downloads file <filename> from server)"
        print "ftp> put <filename> (uploads file <filename> to server)"
        print "ftp> ls (list files on server)"
        print "ftp> lls (lists files on the client)"
        print "ftp> quit (disconnect)"
        print "ftp> help (displays commands)\n"

def serverDirectoryListing(clientSocket, serverAddress):
    #ephemeral Setup
    print "Data Connection Setup"
    ephemPort = clientSocket.recv(SERVER_MSG_SIZE)
    print "Data Connection: " + serverAddress + "at port "+str(ephemPort)
    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    newSocket.connect((serverAddress, int(ephemPort)))
    print "Connected"

    numberOfFiles = newSocket.recv(SERVER_MSG_SIZE)
    print  "files located on server directory = " + numberOfFiles
    #Confirm Received
    newSocket.send(str(numberOfFiles))
    if (int(numberOfFiles != 0 )):

        receivedFiles = 0
        while(int(receivedFiles) <= int(numberOfFiles)):
            fileName = newSocket.recv(SERVER_MSG_SIZE)
            receivedFiles +=1
            if not fileName:
                break

            print fileName
            #verify that we received data
            newSocket.send(fileName)
            # newSocket.send(str(receivedFiles))

    else:
        print 'No files listed'
    print 'Closing Data connection \n'
    newSocket.close()
    print 'Data connection closed'




def main():

    # Get the host name (or IP)
    serverAddress = "localHost"

    # Get the server's port number
    serverPort = 1200

    # The size of the message sent by server
    SERVER_MSG_SIZE = 1024


    # The client socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server */
    print "Connecting to " + str(serverAddress) + " on port " + str(serverPort)
    clientSocket.connect((serverAddress,serverPort))
    print "Connected to server"


    displayCommands()
    while (1):


        userInput = raw_input("ftp> ")

        if(userInput == "quit"):
            print "Closing Connection..."
            clientSocket.send(userInput)
            clientSocket.close()
            print "Connection Closed"
            break
        elif (userInput == "ls"):
            clientSocket.send(userInput)
            serverDirectoryListing(clientSocket, serverAddress)

        elif (userInput == "lls"):
            clientLocalListing()
        elif (userInput == "help"):
            displayCommands()
        else:
            print("Error: Invalid Command.")


if __name__ == '__main__':
    main()

    #
    #
    # # Send a string to the server
    # clientSocket.send(testVar)
    #
    # # Get the date from the server
    # data = clientSocket.recv(SERVER_MSG_SIZE)
    #
    # print 'Received:', data, ' from the server'
    #
    # # Close the connection to the server
    # clientSocket.close()
