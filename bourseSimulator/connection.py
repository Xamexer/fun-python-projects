import socket
from sys import argv

class UdpSocket:
    def __init__(self, address, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = address
        self.port = port
        pass
    
    def bind(self):
        self.sock.bind((self.address, self.port))

    def receive(self, byteamount = 1024):
        data, addr = self.sock.recvfrom(byteamount)
        return (data, addr)

    def send(self, message):
        self.sock.sendto(message,(self.address, self.port))
