import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")

disconnected=True


# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

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

def write():
    while True:
        message = '{}%{}: {}'.format(input(),nickname.upper(),input())
        client.send(my_code(message,key).encode('ascii'))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = my_decode(client.recv(1024).decode('ascii'),key)
            if message == 'NICK':
                client.send(my_code(nickname,key).encode('ascii'))
            else:
                if message=='Connected to server!':
                    write_thread = threading.Thread(target=write)
                    write_thread.start()
                print(f"\n{message}\n")
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break;



# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()




