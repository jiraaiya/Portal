from fastapi import APIRouter, Depends, HTTPException, Header
from app.services.jira_service import get_jira_issues, create_jira_ticket, get_jira_issue_by_key, transition_jira_issue, get_issue_transitions
from app.models import IssueCreate
# from app.utils.auth import get_current_user_token
from typing import Optional

router = APIRouter()

def get_token_from_header(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return authorization.split(" ")[1]

@router.get("/dashboard")
async def dashboard(
    jql_query: str,
    authorization: Optional[str] = Header(None)
):
    """Retrieve Jira issues."""
    token = get_token_from_header(authorization)
    issues = get_jira_issues(jql_query=jql_query, access_token=token)
    if issues:
        return {"issues": issues}
    else:
        raise HTTPException(status_code=400, detail="No issues found")

@router.post("/create_ticket")
async def create_ticket(
    issue: IssueCreate,
    authorization: Optional[str] = Header(None)
):
    """Create a new Jira issue."""
    token = get_token_from_header(authorization)
    result = create_jira_ticket(issue, access_token=token)
    if result:
        return {"message": "Issue created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to create issue")

@router.get("/transitions/{issue_key}")
async def get_transitions(
    issue_key: str,
    authorization: Optional[str] = Header(None)
):
    """Get available transitions for a Jira issue."""
    token = get_token_from_header(authorization)
    transitions = get_issue_transitions(issue_key, access_token=token)
    if "error" in transitions:
        raise HTTPException(status_code=400, detail=transitions["error"])
    return {"transitions": transitions}

@router.post("/transition/{issue_key}")
async def transition_issue(
    issue_key: str,
    transitionId: dict,
    authorization: Optional[str] = Header(None)
):
    """Transition a Jira issue to a new status."""
    token = get_token_from_header(authorization)
    result = transition_jira_issue(issue_key, transitionId["transitionId"], access_token=token)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Issue transitioned successfully"}

@router.get("/issues/{issue_key}")
async def fetch_issue(
    issue_key: str,
    authorization: Optional[str] = Header(None)
):
    """Fetch a single Jira issue by key."""
    token = get_token_from_header(authorization)
    issue = get_jira_issue_by_key(issue_key, access_token=token)
    if issue:
        return issue
    raise HTTPException(status_code=404, detail="Issue not found")