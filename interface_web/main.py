# interface_web/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from pathlib import Path

from agent.supervisor import handle_user_input


app = FastAPI()

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Connected client storage
chat_clients = set()
log_clients = set()

@app.get("/")
async def get():
    with open(static_dir / "index.html", "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    chat_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo for now (hook up agent later)
            response = handle_user_input(data)
            await websocket.send_text(f"🤖 {response}")
    except WebSocketDisconnect:
        chat_clients.remove(websocket)

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    log_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # hold connection open
    except WebSocketDisconnect:
        log_clients.remove(websocket)

# Logger API for supervisor or tools to use
async def log_message(message: str):
    for ws in list(log_clients):
        try:
            await ws.send_text(message)
        except:
            log_clients.discard(ws)

if __name__ == "__main__":
    uvicorn.run("interface_web.main:app", host="127.0.0.1", port=8175, reload=True)