# SL Chat — Phase 3 (FastAPI + WebSocket)

## Eka Run Karanne Kohomada?

### 1. Folder eka yanna
```bash
cd phase3-chat-app
```

### 2. Virtual environment ekak hadanna (recommended)
```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Dependencies install karanna
```bash
pip install -r requirements.txt
```

### 4. Server eka start karanna
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Browser eka open karanna
```
http://127.0.0.1:8000
```

Tab/window godak open karala, username wenas wenas danna —
real-time chat eka test karanna puluwan.

## LAN ekema thawa kenek ekka test karanna

1. Oyage computer eke IP address eka hoyaganna:
   - Mac/Linux: `ifconfig` or `ip addr`
   - Windows: `ipconfig`
2. Thawa kenekta `http://<oyage-ip>:8000` kiyala denna
   (okkoma WiFi/network ekema thiyenna one).

## File Structure

```
phase3-chat-app/
├── main.py            # FastAPI server + WebSocket logic
├── requirements.txt
└── static/
    ├── index.html      # Chat UI
    ├── style.css        # Styling
    └── script.js         # WebSocket client logic
```