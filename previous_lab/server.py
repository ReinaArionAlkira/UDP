import socket
import sys
import random
import os

# Ip of server
localIP = "127.0.0.1"
localPort = 2122

# Getting values from params
# First client
ip1 = "127.0.0.1"
port1 = 1338

bufferSize = 1024

# Second client
ip2 = "127.0.0.1"
port2 = 1339

# probability of noise
probability = 0.1

# Creating socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Binding IP
UDPServerSocket.bind((localIP, localPort))
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
    (messageRaw, remoteAddress) = UDPServerSocket.recvfrom(bufferSize)
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
    if remoteHost == ip1 and remotePort == port1:
        UDPServerSocket.sendto(messageRaw, (ip2, port2))
    else:
        UDPServerSocket.sendto(messageRaw, (ip1, port1))

