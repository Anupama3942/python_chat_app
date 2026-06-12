import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

# Receive messages 
def receive_messages():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            print(data.decode('utf-8'))
        except:
            break

# start receiving thread

recv_thread = threading.Thread(target=receive_messages)
recv_thread.daemon = True
recv_thread.start()

# main loop

while True:
    try:
        msg = input()
        if msg.lower() == "quit":
            break
        client.send(msg.encode('utf-8'))
    except:
        break

client.close()
print("Disconnected from server.") 