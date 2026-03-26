import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8888))

while True:
    message = input('client: ')
    client.send(message.encode('utf-8'))
    
    if message == 'exit':
        break
    
    response = client.recv(1024).decode('utf-8')
    print(f'server {response}')

client.close()