import sys
import os

# Add the parent directory to sys.path to make absolute imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel,Field
from typing import List, Literal, Optional
from datetime import datetime
from backend_ai.config import *

class Chat(BaseModel):
    sender: Literal["user", "model"]
    message: str
    timestamp: datetime = datetime.utcnow()

class ChatStream(BaseModel):
    id: str
    userId: str
    chats: List[Chat] = []

class User(BaseModel):
    id: Optional[str] = Field(None, alias="uid")
    name: str
    email: str
    password: str  
    chatStreams: List[str] = []  

class FirestoreDB:
    def __init__(self, db):
        self.db = db

    async def create_user(self, user: User) -> str:
        """Create a new user"""
        user_ref = self.db.collection("users").document(user.id)
        user_ref.set(user.dict())
        return user.id

    async def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        doc = self.db.collection("users").document(user_id).get()
        if doc.exists:
            return User(**doc.to_dict())
        return None

    async def create_chat_stream(self, user_id: str) -> str:
        """Create a new chat stream"""
        chat_stream = ChatStream(
            id=self.db.collection("chatStreams").document().id,
            userId=user_id,
            chats=[]
        )

        self.db.collection("chatStreams").document(chat_stream.id).set(
            chat_stream.dict()
        )

        user_ref = self.db.collection("users").document(user_id)
        user_ref.update({
            "chatStreams": firestore.ArrayUnion([chat_stream.id])
        })
        
        return chat_stream.id

    async def add_chat_to_stream(self, stream_id: str, chat: Chat):
        """Add a chat message to a stream"""
        chat_ref = self.db.collection("chatStreams").document(stream_id)
        chat_ref.update({
            "chats": firestore.ArrayUnion([chat.dict()])
        })

    async def get_chat_stream(self, stream_id: str) -> Optional[ChatStream]:
        """Get chat stream by ID"""
        doc = self.db.collection("chatStreams").document(stream_id).get()
        if doc.exists:
            return ChatStream(**doc.to_dict())
        return None

    async def get_user_chat_streams(self, user_id: str) -> List[ChatStream]:
        """Get all chat streams for a user"""
        user = await self.get_user(user_id)
        if not user:
            return []
        
        streams = []
        for stream_id in user.chatStreams:
            stream = await self.get_chat_stream(stream_id)
            if stream:
                streams.append(stream)
        return streams
