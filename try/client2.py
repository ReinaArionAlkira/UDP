import my_socket
import time
import threading
import sys

# Port for client
port = 1338

server = '127.0.0.1:2122'
server_host, server_port = server.split(':')
server_port = int(server_port)

receiver = "127.0.0.1:1339"
receiver_host, receiver_port = receiver.split(":")
receiver_port = int(receiver_port)

# Creating socket
sock = my_socket.MySocket()
# Binding ip
sock.bind((receiver_host, receiver_port))
print(f"Bound on {receiver}")


# Defining threading
def recvloop():
    while True:
        (data, _) = sock.recvfrom(1024)
        response = data.decode('utf-8', 'ignore')
        print("[SERV]: {}".format(response))


t = threading.Thread(target=recvloop)
t.start()

while True:
    message = input()
    raw = message.encode()
    sock.sendto(raw, (server_host, server_port))
    time.sleep(0.1)
