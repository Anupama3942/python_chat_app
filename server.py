import socket

server = socket.socket(socket.AF_INET, socket.SOCK.STREAM)

# socket.AF_INET => we use IPv4 
# socket.SOCK.STREAM => we use TCP 

server.bind(('127.'))