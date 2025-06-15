from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse("""
    <html>
        <body>
            <h1>WebSocket Echo Test</h1>
            <input id="message" type="text" />
            <button onclick="sendMessage()">Send</button>
            <ul id="messages"></ul>
            <script>
                var ws = new WebSocket("ws://localhost:8000/ws");
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    message.innerText = event.data;
                    messages.appendChild(message);
                };
                function sendMessage() {
                    var input = document.getElementById("message");
                    ws.send(input.value);
                    input.value = '';
                }
            </script>
        </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Cliente desconectado")
