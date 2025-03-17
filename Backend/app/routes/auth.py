from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_service import authenticate_jira_user

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    user = authenticate_jira_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user": user}
