import socket
import struct
import cv2

bufferSize = 1024
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005
listeningAddress = (SERVER_IP, SERVER_PORT)

pcSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pcSocket.bind(listeningAddress)
print('Listening at:',listeningAddress)


while True:
    print('here')
    conn, addr = pcSocket.recvfrom(1024)
    print("recieve")
    message = struct.unpack_from('>i', bytearray(conn))
    print(type(message))
    print(message)