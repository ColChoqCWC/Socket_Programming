#python HTTPClient.py www.cnn.com 80 GET index.html

#imports the socket, sys, and requests libraries
import socket
import sys
import requests

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a socket
commands = sys.argv #gets command line arguments

#function that checks if a file exsits
def check_file(file):
    try:
        open(file, "r")
        return False
    except:
        return True

host = commands[1] #the host argument
port = int(commands[2]) #the port argument
action = commands[3] #the action argument
filename = commands[4] #the file argument
#print(commands)

if host == 'LocalHost': #checks if the host argument is the localhost

    connection = s.connect_ex((host, port)) #connects to the server and gets the connection number
    print("Connected to Server:", host, ",", port)
    sendComm = ""
    for x in commands: #puts the comments in to a str to send to the server
        sendComm += x + " "
    #print(sendComm.strip())
    s.send(sendComm.strip().encode()) #send the command line arguments to the server

    if commands[3] == 'GET': #if the action argument is get
        print("GET Executed")
        check = s.recv(1024).decode() #gets a check message forom the client
        if check == "success":
        
            file1 = open(commands[4], "w") #opens a file to write

            data1 = s.recv(1024).decode() #gets the data from the server
            #print(data1)
            print("File and Data Received")

            file1.write(data1) #writes the data to the file

            if connection == 0: #if the connection is good then everything is successfull
                print("Success")
            file1.close() #closes the file
            s.close() #closes the connection
        else: #if the server connection is bad
            print("404 Not Found: File Error")
            s.send("fail".encode())
            s.close()
    


    elif commands[3] == 'PUT': #checks if the action is a put
        print("PUT Executed")
        if check_file(filename) != True: #checks if the file exsits
            s.send("success".encode()) #sends a success tot he server
            file = open(filename, "r") #opens the client file
            data = file.read() #reads the files data
            file.close() #closes the file
            print("File sending...")
    
            msg = s.recv(1024).decode() #a message if the data and the file where recived
            print(msg)

            s.send(data.encode()) #sends the file data to the server
            if connection == 0: #if the conneciton is good then everything is successful
                print("Success")

            s.close() #closes the conneciton
        else: #if the file is not found
            print("404 Not Found: File Error")
            s.send("fail".encode())

    else: #if the action is not a get or a put
        print("404 Not Found: GET/PUT Error")
else: #if the host is not local
    if host.isdigit(): #if the host is either a ip adress or a website
        ip = socket.gethostbyaddr(commands[1])
    else:
        ip = socket.gethostbyname(commands[1])
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a socket
    
    connected = p.connect_ex((ip,port)) #connects the socket
    #print(connected)

    if connected == 0: #if the connection is good
        url = "http://"+commands[1]+"/"+commands[4] #gets the url from the commadn line arguments

        data = requests.get(url) #gets the data from the url
        #print(data)
        index = open(filename, "wb") #opens a file with binary writing
        #print(data.content)
    
        index.write(data.content) #writes the data to the file
        if data.status_code == 200: #is the data was successfully gotten then is was successful
            print("Success")
        index.close() #closes the file
    else: #if the conneciton was bad
        print("404 Not Found: Command Error")
    s.close #closes the conneciton
