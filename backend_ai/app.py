from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
import os
from backend_ai import model, auth
from backend_ai.model_config import initialize_models
from backend_ai.database import FirestoreDB, User, Chat

# Add the parent directory to sys.path to make absolute imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    initialize_models()

class ChatRequest(BaseModel):
    message: str
    stream_id: str

class PortfolioRequest(BaseModel):
    user_id: str
    ticker: str
    quantity: int
    purchase_price: float

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str  # Will be hashed before storage

@app.post("/api/users")
async def create_user(request: CreateUserRequest):
    try:
        # Create a Firebase user; Firebase generates a unique uid.
        firebase_user = auth.create_user(
            email=request.email,
            password=request.password,
            display_name=request.name,
        )
        
        # Hash the password (if you want to store it separately in your Firestore for other reasons)
        hashed_password = auth.hash_password(request.password)
        
        # Create the user in your Firestore. Map Firebase's uid to the required "id" field.
        new_user = User(
            id=firebase_user.uid,  # Assign Firebase's uid to the required "id" field.
            name=request.name,
            email=request.email,
            password=hashed_password,
            chatStreams=[]
        )
        
        await FirestoreDB.create_user(new_user)
        return {"uid": firebase_user.uid, "email": firebase_user.email, "name": firebase_user.display_name}
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat-streams")
async def create_chat_stream(user=Depends(auth.verify_token)):
    try:
        stream_id = await FirestoreDB.create_chat_stream(user['uid'])
        return {"stream_id": stream_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest, user=Depends(auth.verify_token)):
    try:
        user_chat = Chat(
            sender="user",
            message=request.message
        )
        
        await FirestoreDB.add_chat_to_stream(request.stream_id, user_chat)
        
        response = await model.process_chat(request.message, user['uid'])
        
        ai_chat = Chat(
            sender="model",
            message=response
        )
        await FirestoreDB.add_chat_to_stream(request.stream_id, ai_chat)
        
        return {
            "response": response,
            "chat": ai_chat.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolio/{user_id}")
async def get_portfolio(user_id: str, user=Depends(auth.verify_token)):
    try:
        portfolio = await model.get_user_portfolio(user_id)
        return portfolio
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/portfolio/analyze")
async def analyze_portfolio(request: PortfolioRequest, user=Depends(auth.verify_token)):
    try:
        analysis = await model.analyze_stock_position(
            ticker=request.ticker,
            quantity=request.quantity,
            purchase_price=request.purchase_price
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat-streams/{user_id}")
async def get_user_chat_streams(user_id: str, user=Depends(auth.verify_token)):
    try:
        if user['uid'] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        streams = await FirestoreDB.get_user_chat_streams(user_id)
        return {"streams": [stream.dict() for stream in streams]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat-streams/{stream_id}/chats")
async def get_chat_stream(stream_id: str, user=Depends(auth.verify_token)):
    try:
        stream = await FirestoreDB.get_chat_stream(stream_id)
        if not stream:
            raise HTTPException(status_code=404, detail="Chat stream not found")
        
        if stream.userId != user['uid']:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        return {"chats": [chat.dict() for chat in stream.chats]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))