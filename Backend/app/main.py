from fastapi import FastAPI
from app.routes import auth, jira

app = FastAPI(title="Organizational Portal API")

# Include Routes
app.include_router(auth.router, prefix="/auth")
app.include_router(jira.router, prefix="/jira")

@app.get("/")
def read_root():
    return {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
