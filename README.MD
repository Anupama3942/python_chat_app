# SL Chat — Phase 3 (FastAPI + WebSocket)

## How to Run

### 1. Navigate to the project folder
```bash
cd phase3-chat-app
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open the application in your browser
```
http://127.0.0.1:8000
```

Open multiple browser tabs or windows and use different usernames to test the real-time chat functionality.

## Testing with Another Device on the Same LAN

1. Find your computer's IP address:
   - Mac/Linux: `ifconfig` or `ip addr`
   - Windows: `ipconfig`

2. Share the following URL with another user:
   ```
   http://<your-ip>:8000
   ```

3. Ensure both devices are connected to the same Wi-Fi network or local network.

## File Structure

```text
phase3-chat-app/
├── main.py             # FastAPI server + WebSocket logic
├── requirements.txt
└── static/
    ├── index.html      # Chat user interface
    ├── style.css       # Styling
    └── script.js       # WebSocket client logic
```
