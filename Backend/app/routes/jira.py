from fastapi import APIRouter, Depends, HTTPException
from app.services.jira_service import get_jira_issues, create_jira_ticket
from app.models import IssueCreate
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/dashboard")
async def dashboard():
    """Retrieve Jira issues."""
    issues = get_jira_issues(jql_query="status is not empty")
    if issues:
        return {"issues": issues}
    else:
        raise HTTPException(status_code=400, detail="No issues found")

@router.post("/create_ticket")
async def create_ticket(issue: IssueCreate):
    """Create a new Jira issue."""
    result = create_jira_ticket(issue)
    if result:
        return {"message": "Issue created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to create issue")
