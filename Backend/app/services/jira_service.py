import requests
from app.config import settings

def get_jira_issues(jql_query):
    """Fetch Jira issues based on the provided JQL query and return simplified structure."""
    jira_url = f"{settings.jira_url}/rest/api/latest/search"

    headers = {
        "Authorization": f"Bearer {settings.jira_api_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {
        "jql": jql_query,
        "maxResults": 50
    }

    response = requests.get(jira_url, headers=headers, params=params)

    if response.status_code == 200:
        raw_issues = response.json().get("issues", [])
        simplified_issues = []

        for issue in raw_issues:
            fields = issue.get("fields", {})
            simplified_issues.append({
                "key": issue.get("key"),
                "summary": fields.get("summary", ""),
                "status": fields.get("status", {}).get("name", ""),
                "assignee": (
                    fields.get("assignee", {}).get("displayName")
                    if fields.get("assignee") else "بدون مسئول"
                )
            })

        return simplified_issues

    print(f"Error fetching issues: {response.status_code} - {response.text}")
    return []

def get_issue_transitions(issue_key):
    """Get available transitions for a Jira issue."""
    jira_url = f"{settings.jira_url}/rest/api/latest/issue/{issue_key}/transitions"
    
    headers = {
        "Authorization": f"Bearer {settings.jira_api_token}",
        "Accept": "application/json"
    }

    response = requests.get(jira_url, headers=headers)

    if response.status_code == 200:
        transitions = response.json().get("transitions", [])
        return [
            {
                "id": t.get("id"),
                "name": t.get("name"),
                "to_status": t.get("to", {}).get("name")
            }
            for t in transitions
        ]
    return {
        "error": f"Error fetching transitions: {response.status_code} - {response.text}",
        "transitions": []
    }




def create_jira_ticket(issue):
    """Create a new Jira issue."""
    jira_url = f"{settings.jira_url}/rest/api/2/issue"
    # auth = (settings.jira_username, settings.jira_api_token)
    headers = {
        "Authorization": f"Bearer {settings.jira_api_token}",
        "Accept": "application/json"
    }
    data = {
        "fields": {
            "project": {"key": issue.project_key},
            "summary": issue.summary,
            "description": issue.description,
            "issuetype": {"name": issue.issue_type}
        }
    }
    
    response = requests.post(jira_url, headers=headers, json=data)
    if response.status_code == 201:
        return True
    return False

def transition_jira_issue(issue_key, transition_id):
    """Transition a Jira issue to a new status."""
    jira_url = f"{settings.jira_url}/rest/api/latest/issue/{issue_key}/transitions"
    
    headers = {
        "Authorization": f"Bearer {settings.jira_api_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "transition": {
            "id": transition_id
        }
    }

    response = requests.post(jira_url, headers=headers, json=data)

    if response.status_code == 204:  # Jira returns 204 No Content on successful transition
        return True
    return {
        "error": f"Error transitioning issue: {response.status_code} - {response.text}",
        "success": False
    }


import requests
from app.config import settings

def get_jira_issue_by_key(issue_key: str):
    """Fetch a single Jira issue by its issue key."""
    jira_url = f"{settings.jira_url}/rest/api/latest/issue/{issue_key}"

    headers = {
        "Authorization": f"Bearer {settings.jira_api_token}",
        "Accept": "application/json"
    }

    response = requests.get(jira_url, headers=headers)

    if response.status_code == 200:
        return response.json()

    print(f"Failed to fetch issue: {response.status_code} - {response.text}")
    return None
