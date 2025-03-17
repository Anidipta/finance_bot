from firebase_admin import auth
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Dict, Any

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """Verify Firebase JWT token"""
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        return decoded_token
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