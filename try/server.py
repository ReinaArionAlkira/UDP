import my_socket
import sys
import random
import os

# Ip of server
server = '127.0.0.1:2122'
server_host, server_port = server.split(':')
server_port = int(server_port)

# First client
sender = '127.0.0.1:1338'
sender_host, sender_port = sender.split(':')
sender_port = int(sender_port)

bufferSize = 1024

# Second client
receiver = "127.0.0.1:1339"
receiver_host, receiver_port = receiver.split(":")
receiver_port = int(receiver_port)

# probability of noise
probability = 0.1

# Creating socket
server_socket = my_socket.MySocket()

# Binding IP
server_socket.bind((server_host, server_port))
print("UDP server up and listening")

def corruptData(data):
    # If the probability is given, we randomly exchange bytes
    if probability > 0:
        for i in data:
            # We draw from the range 0-1 and compare the received number with the given probability
            # If the given probability is higher, we replace the bytes with random ones
            if random.random() < probability:
                data = data.replace(i.to_bytes(), os.urandom(1), 1)
        return data
    else: return data

# Listening loop
while True:
    # Receiving message
    (messageRaw, remoteAddress) = server_socket.recvfrom(bufferSize)
    (remoteHost, remotePort) = remoteAddress

    message = messageRaw.decode()

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(remoteAddress)

    # Printing information to the console
    print(clientMsg)
    print(clientIP)
    print(messageRaw)

    # Corrupting Data with given probability
    messageRaw = corruptData(messageRaw)

    # Sending a message to the second client
    if remoteHost == sender_host and remotePort == sender_port:
        server_socket.sendto(messageRaw, (receiver_host, receiver_port))
    else:
        server_socket.sendto(messageRaw, (sender_host, sender_port))

