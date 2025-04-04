from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from model import process_chat  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    id: str

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             # Receive message from the client.
#             data = await websocket.receive_text()

#             try:
#                 # Process the chat message (process_chat returns [intent, response]).
#                 response_data = await process_chat(data)
#                 # Send response back to the client.
#                 await websocket.send_json({
#                     "intent": response_data[0],
#                     "response": response_data[1]
#                 })
#             except Exception as e:
#                 # Send an error response.
#                 await websocket.send_json({
#                     "error": f"Error processing message: {str(e)}"
#                 })
#     except WebSocketDisconnect:
#         print("WebSocket connection closed.")

# @app.get("/")
# async def get():
#     try:
#         with open("frontend.html", "r") as f:
#             content = f.read()
#         return HTMLResponse(content=content, status_code=200)
#     except Exception as e:
#         return HTMLResponse(content=f"Error loading frontend: {str(e)}", status_code=500)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response_data = await process_chat(request.message,request.id)
        return {
            "intent": response_data[0],
            "response": response_data[1]
        }
    except Exception as e:
        return {"error": f"Error processing chat request: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
