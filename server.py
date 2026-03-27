import socket
import threading
from datetime import datetime

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# time = datetime.now().strftime("%H:%M:%S")

# socket.AF_INET => we use IPv4 
# socket.SOCK.STREAM => we use TCP 

server.bind(('', 1112))

server.listen(1) # max connections = 1
print("server is ready! wait for client....")

conn, addr = server.accept() # conn = socket object for client connection, addr = client address
print(f"client connected: {addr}")

user_name = conn.recv(1024).decode('utf-8')
if not user_name:
    user_name = "unknown"
print(f"{user_name} is connected.")

def recieve_message():
    
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            time = datetime.now().strftime("%H:%M:%S")
            print(f"\n{time} {user_name}: {data.decode('utf-8')}")
            print("server: ", end="")
            
            if data.decode('utf-8') == "exit":
                print("client disconnected")
                break
        
        except Exception as e:
            print(f"Error {e}")
            break
        
t = threading.Thread(target=recieve_message)
t.start()

while True:
    msg = input("server: ")
    if msg == "exit":
        conn.send("Goodbye..!".encode('utf-8'))
        break
    conn.send(msg.encode('utf-8'))
    
conn.close()
server.close()