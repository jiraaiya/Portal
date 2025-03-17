from fastapi import APIRouter
from app.services.jira_service import get_jira_issues

router = APIRouter()

@router.get("/issues")
def get_issues(jql: str):
    return get_jira_issues(jql)
