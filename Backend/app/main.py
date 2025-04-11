from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, jira
from app.config import settings
from app.database import get_db
from sqlalchemy.orm import Session

app = FastAPI(title="Organizational Portal")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://local.myapp.com:3000",  # Frontend URL
        "http://localhost:3000",         # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes from auth and jira modules
app.include_router(auth.router)
app.include_router(jira.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
