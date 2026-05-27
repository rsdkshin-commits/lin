from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, Set
import json
import uuid
from datetime import datetime

app = FastAPI(title="Interactive Remote Notify")

app.mount("/static", StaticFiles(directory="static"), name="static")

clients: Dict[str, Dict] = {}


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.get("/manifest.json")
async def manifest():
    return FileResponse("static/manifest.json")


@app.get("/sw.js")
async def service_worker():
    return FileResponse("static/sw.js")


async def broadcast(target_role: str, payload: dict):
    disconnected = []
    for client_id, item in clients.items():
        if item["role"] == target_role:
            try:
                await item["ws"].send_text(json.dumps(payload, ensure_ascii=False))
            except Exception:
                disconnected.append(client_id)

    for client_id in disconnected:
        clients.pop(client_id, None)


@app.websocket("/ws/{role}")
async def websocket_endpoint(websocket: WebSocket, role: str):
    await websocket.accept()

    if role not in ["sender", "receiver"]:
        await websocket.close()
        return

    client_id = str(uuid.uuid4())
    clients[client_id] = {
        "ws": websocket,
        "role": role,
        "joined_at": datetime.now().isoformat()
    }

    await websocket.send_text(json.dumps({
        "type": "system",
        "message": f"已連線：{role}",
        "role": role
    }, ensure_ascii=False))

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            msg_type = data.get("type")
            text = data.get("message", "")

            if not text:
                continue

            if role == "sender" and msg_type == "request":
                await broadcast("receiver", {
                    "type": "request",
                    "from": "發送方",
                    "message": text,
                    "voice": f"有新的請求：{text}",
                    "time": datetime.now().strftime("%H:%M:%S")
                })

            elif role == "receiver" and msg_type == "reply":
                await broadcast("sender", {
                    "type": "reply",
                    "from": "接收方",
                    "message": text,
                    "voice": f"接收方回覆：{text}",
                    "time": datetime.now().strftime("%H:%M:%S")
                })

    except WebSocketDisconnect:
        clients.pop(client_id, None)
    except Exception:
        clients.pop(client_id, None)
        try:
            await websocket.close()
        except Exception:
            pass
