from firebase_admin import auth
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Dict, Any
import jwt  # Ensure to install the 'pyjwt' package
import bcrypt

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """Verify Firebase JWT token"""
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # Contains 'uid', 'email', etc.
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}"
        )

async def get_user_claims(token: str) -> Dict[str, Any]:
    """Get custom claims from Firebase token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token.get("claims", {})
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error getting user claims: {str(e)}"
        )

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
