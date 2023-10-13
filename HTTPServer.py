#C:\Users\colin\OneDrive\Desktop\CSC\544\Assigh4\HTTPServer
#python HTTPServer.py 50000

#import the socket and sys libraries
import socket
import sys


command = sys.argv #grabs the comand line arguments
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a socket
#print("Socket made")

#this is a function that checks if the file is in the server
def check_file(file):
    try:
        open(file, "r")
        return False
    except:
        return True


#grabs the port number from the command line
port = int(command[1])
print("Server is Using Port:", port)

#binds the port to the socket
s.bind(('', port))
#print("socket binded to ",port)

#makes the socket listen for a server
s.listen(5)
print("Server is Listneing...")

#while a client is connected
while True:
    conn, addr = s.accept() #acctept the connection
    print('Connection Made From', addr)
    
    commandRec = conn.recv(1024).decode().split(" ") # gets the comand line arguments from the client
    #print(commandRec)


    if commandRec[3] == "GET": #check if the commadn line has GET
        if check_file(commandRec[4]) != True: #calls the function to check if the file exists
            conn.send("success".encode()) #sends a success to the client
            file1 = open(commandRec[4], "r") #reads the file called in the client command line
            data1 = file1.read() #reads the data from the file
            print("Sending File...")

            conn.send(data1.encode()) #sends the data of the file to the client
            print("File Sent To:", addr)
            file1.close() #closes the file

            print("")
            print("--------------------------------------------------------------------------------------------------------")
            print("")

            conn.close() #closes the connection
            break
        else: #if the file is not found
            print("File Error")
            conn.send("fail".encode())
            break



    if commandRec[3] == "PUT": #checks if the command line has PUT
        check = conn.recv(1024).decode() #gets a check message forom the client
        if check == "success": #if the check is not fail
            file = open(commandRec[4], "w") #opens a fiel to write
            conn.send("File was Received".encode()) #sends the client that the file was recived

            data = conn.recv(1024).decode() #recives the data from the client
            print("File Received From:", addr)

            file.write(data) #writes the data to the file


            print("")
            print("--------------------------------------------------------------------------------------------------------")
            print("")

            file.close() #closes the file
            conn.close() #closes the connection
            break
        else: #if the check is fail
            print("file error")
            break
        
