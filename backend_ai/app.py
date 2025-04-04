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
