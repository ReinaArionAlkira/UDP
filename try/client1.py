import my_socket
import time
import threading
import sys
import signal
import os

def signal_handler(signal, frame):
        # close the socket here
        os._exit(0)
signal.signal(signal.SIGINT, signal_handler)


server = '127.0.0.1:2122'
server_host, server_port = server.split(':')
server_port = int(server_port)

sender = '127.0.0.1:1338'
sender_host, sender_port = sender.split(':')
sender_port = int(sender_port)

# Creating socket
sock = my_socket.MySocket()

# Binding ip
sock.bind((sender_host, sender_port))
print(f"Bound on {sender}")


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
