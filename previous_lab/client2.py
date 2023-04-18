import socket
import time
import threading
import sys

# Port for client
port = 1338

# Getting values from params
(servIP, servPort) = sys.argv[1], int(sys.argv[2])

# Creating socket
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Binding ip
sock.bind(("127.0.0.1", port))
print("Bound on {}".format(port))


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
    sock.sendto(raw, (servIP, servPort))
    time.sleep(0.1)
