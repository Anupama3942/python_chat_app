# phase 3 - FastAPI + WebSocket Chat Server

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime

app = FastAPI(title = "WebSocket Chat Server")
app.mount("/static", StaticFiles(directory="static"), name="static")

# connection manager to handle multiple clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, str] = {}
        
    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[websocket] = username
        
    def disconnect(self, websocket: WebSocket):
        return self.active_connections.pop(websocket, None)
    
    async def broadcast(self, message: dict, exclude: WebSocket = None):
        
        dead_connections = []
        for connection in list(self.active_connections.keys()):
            if connection is exclude:
                continue
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)
        
        for conn in dead_connections:
            self.self.active_connections.pop(conn, None)
    
    def user_list(self):
        return list(self.active_connections.values())
    
manager = ConnectionManager()

@app.get("/")
async def get_index():
    # Browesr will load the index.html file from the static folder
    return FileResponse("static/index.html")

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    # asyncio event loop use and FastAPI use single thread to handle multiple clients concurrently
    
    await manager.connect(websocket, username)
    
    join_time = datetime.now().strftime("%H:%M:%S")
    await manager.broadcast(
        {"type": "system", "text": f"{username} has joined to the chat!", "time": join_time},
         exclude = websocket,
    )
    
    await manager.broadcast({"type": "user_list", "users": manager.user_list()})
    
    try:
        while True:
            data = await websocket.receive_text()
            msg_time = datetime.now().strftime("%H:%M:%S")
            await manager.broadcast(
                {
                    "type": "message",
                    "user": username,
                    "text": data,
                    "time": msg_time
                }
            )
    except WebSocketDisconnect:
        # when clien close browser or disconnect from the server, WebSocketDisconnect exception will be raised
        manager.disconnect(websocket)
        leave_time = datetime.now().strftime("%H:%M:%S")
        await manager.broadcast(
            {"type": "system",
             "text": f"{username} has left the chat!",
             "time": leave_time}
        )
        
        await manager.broadcast(
            {
                "type": "user_list",
                "users": manager.user_list()
            }
        )