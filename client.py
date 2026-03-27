import socket
import threading
from datetime import datetime

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1112))

time = datetime.now().strftime("%H:%M:%S")

name = input("Enter your name: ")
client.send(name.encode('utf-8'))

def receive_message():
    
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            print(f"{time} server: {data.decode('utf-8')}")
        except:
            break

def save_log(message):
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

t = threading.Thread(target=receive_message)
t.start()

while True:
    msg = input("client: ")
    if msg == "exit":
        break
    client.send(msg.encode('utf-8'))
    save_log(f"[{time}] client: {msg}")
    
client.close()
