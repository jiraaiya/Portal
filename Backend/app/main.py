from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, jira
from app.config import settings

app = FastAPI(title="Organizational Portal")

# CORS settings
origins = [
    "http://localhost:5173",  # React dev server
    # "http://localhost:3000",  # Alternative React port
    # "https://127.0.0.1:8443",  # Jira server
    "https://local.myapp.com:3000",  # Custom domain for OAuth callback
    "http://localhost:8000",  # Backend server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Which frontend domains can access this backend
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)
# Include the routes from auth and jira modules
app.include_router(auth.router)
app.include_router(jira.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
