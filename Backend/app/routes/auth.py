from fastapi import APIRouter, HTTPException
from app.services.auth_service import authenticate_user
from app.models import UserCredentials

router = APIRouter()

@router.post("/login")
async def login(credentials: UserCredentials):
    """Authenticate the user with Jira API credentials."""
    if authenticate_user(credentials):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
