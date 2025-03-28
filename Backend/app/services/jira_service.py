import requests
from app.config import settings

def get_jira_issues(jql_query):
    """Fetch Jira issues based on the provided JQL query."""
    jira_url = f"{settings.jira_url}/rest/api/latest/search"
    
    # Set the headers with Authorization Bearer token
    headers = {
        "Authorization": f"Bearer {settings.jira_api_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Set the JQL query parameters
    params = {
        "jql": jql_query,
        "maxResults": 50
    }
    print("step 1")
    # Send the GET request to Jira API
    response = requests.get(jira_url, headers=headers, params=params)
    print("step 2")

    # Check if the response was successful
    if response.status_code == 200:
        return response.json()["issues"]
    
    # In case of failure, print the error message for debugging
    print(f"Error fetching issues: {response.status_code} - {response.text}")
    return None


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
