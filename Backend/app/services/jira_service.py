from jira import JIRA
from app.config import JIRA_URL, JIRA_USER, JIRA_API_TOKEN

def get_jira_issues(jql: str):
    jira = JIRA(server=JIRA_URL, basic_auth=(JIRA_USER, JIRA_API_TOKEN))
    issues = jira.search_issues(jql, maxResults=10)
    return [{"key": issue.key, "summary": issue.fields.summary} for issue in issues]
