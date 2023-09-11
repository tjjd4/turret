import socket
import struct
import cv2

bufferSize = 1024
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005
listeningAddress = (SERVER_IP, SERVER_PORT)

pcSocket = socket.socket(socket.AF_INET, socket.NI_DGRAM)
pcSocket.bind(listeningAddress)
print('PC Socket is up and listening to 192.168.0.118:2222')

pcSocket.listen(10)

while True:
    conn, addr = pcSocket.accept()
    message = struct.unpack_from('>i', bytearray(conn))
    print(type(message))
    print(message)