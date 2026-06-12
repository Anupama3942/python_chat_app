import socket
import threading

clients = {}

# Broadcast message to all clients
def broadcast(message, sender_conn=None):
    for conn in list(clients.keys()):
        if conn != sender_conn:
            try:
                conn.send(message.encode('utf-8'))
            except:
                clients.pop(conn, None)
                
# handle single client connection

def handle_client(conn, addr):
    try:
        conn.send("Welcome to the chat! Please enter your username: ".encode('utf-8'))
        userName = conn.recv(1024).decode('utf-8').strip()
        
        clients[conn] = userName
        print(f"[+] {userName} has connected from {addr}")
        
        broadcast(f"{userName} has joined the chat!", conn)
        
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode('utf-8')
            if msg.lower() == "quit":
                break
            
            full_msg = f"[{userName}] : {msg}"
            broadcast(full_msg, conn)
            print(full_msg)
    except:
        pass
    
    finally:
        
        userName = clients.pop(conn, '???')
        conn.close()
        broadcast(f"{userName} has left the chat!")
        print(f"[-] {userName} has disconnected from {addr}")
        
#  main server function

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
server.bind(('', 12345))
server.listen(10)

print("Server is listening on port 12345...")

while True:
    
    # if msg.startswith("/list"):
        
    #     # create a string of all clients in the dictionary
        
    #     user_list = ", ".join(clients.values())
    #     response = f"Connected users: {user_list}"
    #     conn.send(response.encode('utf-8'))
    #     continue
    
    conn, addr = server.accept()
    t = threading.Thread(target=handle_client, args=(conn, addr))
    t.deamon = True
    t.start()
    print(f"[Thread] Active : {threading.active_count() - 1}")

                