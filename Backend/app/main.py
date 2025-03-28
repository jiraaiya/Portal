from fastapi import FastAPI
from app.routes import auth, jira
from app.config import settings

app = FastAPI(title="Organizational Portal")

# Include the routes from auth and jira modules
app.include_router(auth.router)
app.include_router(jira.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
