from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
# the code is a simple chat application using FastAPI and WebSockets.
# The code defines a FastAPI application with a single route that returns an HTML page with a chat interface.
# The page contains an input field for sending messages and a list to display received messages.
### to run the code open terminal change the path to the folder where main.py is located and run the following command

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-time Chat</title>
</head>
<body>
    <h1>Real-time Chat</h1>
    <input type="text" id="messageText" />
    <button onclick="sendMessage()">Send</button>
    <ul id="messages"> </ul>
    <script>
        var wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        var wsHost = window.location.hostname;
        var wsPort = window.location.port || '8000'; // Use the page's port or default to 8000
        var ws = new WebSocket(wsProtocol + '//' + wsHost + ':' + wsPort + '/ws');
        
        // Listen for messages from the server
        ws.onmessage = function(event) {
            var messages = document.getElementById('messages');
            var message = document.createElement('li');
            message.textContent = event.data;
            messages.appendChild(message);
        };

        // Send the message from the input box to the server
        function sendMessage() {
            var input = document.getElementById('messageText'); // Fixed input ID
            ws.send(input.value);  // Send the value to the WebSocket server
            input.value = '';      // Clear the input field after sending
        }
    </script>
</body>
</html>
"""

@app.get("/")
def get():
    return HTMLResponse(html)


clients = [] 

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket) # Store the WebSocket connection
    try :
        while True:
            data = await websocket.receive_text()  # Receive message from client
            print(f"Received message: {data}")  # Log to the terminal
            for client in clients:
                await client.send_text(f"Message text was: {data}")  # Broadcast the message to all clients
    except WebSocketDisconnect:
        clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
