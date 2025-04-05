from fastapi import APIRouter, Depends, HTTPException
from app.services.jira_service import get_jira_issues, create_jira_ticket, get_jira_issue_by_key, transition_jira_issue
from app.models import IssueCreate
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/dashboard")
async def dashboard(jql_query: str):
    """Retrieve Jira issues."""
    issues = get_jira_issues(jql_query=jql_query)
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

@router.get("/transitions/{issue_key}")
async def get_transitions(issue_key: str):
    """Get available transitions for a Jira issue."""
    from app.services.jira_service import get_issue_transitions
    
    transitions = get_issue_transitions(issue_key)
    if "error" in transitions:
        raise HTTPException(status_code=400, detail=transitions["error"])
    return {"transitions": transitions}

@router.post("/transition/{issue_key}")
async def transition_issue(issue_key: str, transitionId: dict):
    """Transition a Jira issue to a new status."""
    
    result = transition_jira_issue(issue_key, transitionId["transitionId"])
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Issue transitioned successfully"}

@router.get("/issues/{issue_key}")
async def fetch_issue(issue_key: str):
    issue = get_jira_issue_by_key(issue_key)
    if issue:
        return issue
    raise HTTPException(status_code=404, detail="Issue not found")