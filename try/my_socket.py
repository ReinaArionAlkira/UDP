import socket

class MySocket:
    def __init__(self):
        self.internal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def bind(self, addr: tuple[str, int]):
        self.internal_socket.bind(addr)
    
    def recvfrom(self, buf_size: int):
        return self.internal_socket.recvfrom(buf_size)

    def sendto(self, msg: str, addr: tuple[str, int]):
        self.internal_socket.sendto(msg, addr)