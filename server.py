#!/bin/python3
import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

key=10

def my_code(message,key):
    arr=[]
    for letter in message:
        arr.append(str(ord(letter)*key))
    return ','.join(arr)

def my_decode(arr,key):
    letters=[]
    for letter in arr.split(','):
        letters.append(chr(int(int(letter)/key)))
    return ''.join(letters)

# Sending Messages To All Connected Clients
def broadcast(message,this_client):
    #print("broadcast")
    for client in clients:
        #print(client)
        if client!=this_client:
            #print("this")
            #print(this_client)
            client.send(my_code(message,key).encode('ascii'))

def sendToClients(message,clients_group):
    #print("sendToClients")
    for client in clients_group:
        #print(client)
        #if client in nicknames:
        temp=nicknames.index(client)
        #print(temp)
        clients[temp].send(my_code(message,key).encode('ascii'))

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = my_decode(client.recv(1024).decode('ascii'),key)
            #print(message)
            clients_group,prop_message=tuple(message.split('%'))
            if clients_group=='':
                broadcast(prop_message,client)
            else:
                sendToClients(prop_message,clients_group.split(','))
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname),client)
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send(my_code('NICK',key).encode('ascii'))
        nickname = my_decode(client.recv(1024).decode('ascii'),key)
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname),client)
        client.send(my_code('Type your target login/s(...,...) and press "Enter". Then type your message',key).encode('ascii'))
        client.send(my_code('Connected to server!',key).encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server if listening...")
receive()
