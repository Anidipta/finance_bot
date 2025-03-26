from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import uvicorn
from model import process_chat  # Import your existing process_chat function

app = FastAPI()

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for chat input
class ChatRequest(BaseModel):
    message: str

# WebSocket endpoint for real-time chat
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Process the chat message
            try:
                # Ensure this returns both intent and response
                response_data = await process_chat(data)
                
                # Send response back to client
                await websocket.send_json({
                    "intent": response_data[0],  # First element is intent
                    "response": response_data[1]  # Second element is response
                })
            except Exception as e:
                # Send error response
                await websocket.send_json({
                    "error": str(e)
                })
    except WebSocketDisconnect:
        print("WebSocket connection closed")

# Route to serve the HTML frontend
@app.get("/")
async def get():
    with open("frontend.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Optional: REST API endpoint if needed
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response_data = await process_chat(request.message)
        return {
            "intent": response_data[0],
            "response": response_data[1]
        }
    except Exception as e:
        return {"error": str(e)}

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)