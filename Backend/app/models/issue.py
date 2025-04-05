from pydantic import BaseModel

class IssueCreate(BaseModel):
    summary: str
    description: str
    project_key: str
    issue_type: str
