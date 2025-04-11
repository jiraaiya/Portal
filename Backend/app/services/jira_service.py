import requests
from app.config import settings
import urllib3
import json

# Disable SSL verification warnings for local development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_jira_issues(jql_query, access_token):
    """Fetch Jira issues based on the provided JQL query and return simplified structure."""
    # Ensure the Jira URL doesn't have trailing slashes
    base_url = settings.jira_url.rstrip('/')
    jira_url = f"{base_url}/rest/api/latest/search"
    
    print(f"Making request to Jira API: {jira_url}")
    print(f"JQL Query: {jql_query}")
    print(f"Token (first 10 chars): {access_token[:10]}...")
    print(f"Full token format: {access_token}")  # Log the full token for debugging

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    print(f"Full headers being sent: {headers}")  # Log the full headers

    params = {
        "jql": jql_query,
        "maxResults": 50
    }

    try:
        # First, try to validate the token by making a request to the Jira API
        validate_url = f"{base_url}/rest/api/latest/myself"
        validate_response = requests.get(validate_url, headers=headers, verify=False)
        
        print(f"Validation response status: {validate_response.status_code}")
        print(f"Validation response headers: {validate_response.headers}")
        print(f"Validation response body: {validate_response.text}")
        
        if validate_response.status_code != 200:
            print(f"Token validation failed: {validate_response.status_code} - {validate_response.text}")
            print(f"Token format: {access_token[:20]}...")
            print(f"Headers: {headers}")
            return []
        
        print("Token validated successfully")
        
        # Now make the actual request for issues
        response = requests.get(jira_url, headers=headers, params=params, verify=False)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response body: {response.text[:500]}...")  # Print first 500 chars of response

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
                    ),
                    "project": fields.get("project", {}).get("name", ""),
                    "issueType": fields.get("issuetype", {}).get("name", "")
                })

            return simplified_issues
        else:
            print(f"Error fetching issues: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Exception in get_jira_issues: {str(e)}")
        return []

def get_issue_transitions(issue_key, access_token):
    """Get available transitions for a Jira issue."""
    jira_url = f"{settings.jira_url}/rest/api/latest/issue/{issue_key}/transitions"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    response = requests.get(jira_url, headers=headers, verify=False)

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

def create_jira_ticket(issue, access_token):
    """Create a new Jira issue."""
    jira_url = f"{settings.jira_url}/rest/api/2/issue"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
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
    
    response = requests.post(jira_url, headers=headers, json=data, verify=False)
    if response.status_code == 201:
        return True
    return False

def transition_jira_issue(issue_key, transition_id, access_token):
    """Transition a Jira issue to a new status."""
    jira_url = f"{settings.jira_url}/rest/api/latest/issue/{issue_key}/transitions"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "transition": {
            "id": transition_id
        }
    }

    response = requests.post(jira_url, headers=headers, json=data, verify=False)

    if response.status_code == 204:  # Jira returns 204 No Content on successful transition
        return True
    return {
        "error": f"Error transitioning issue: {response.status_code} - {response.text}",
        "success": False
    }

def get_jira_issue_by_key(issue_key: str, access_token: str):
    """Fetch a single Jira issue by its issue key."""
    jira_url = f"{settings.jira_url}/rest/api/latest/issue/{issue_key}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    response = requests.get(jira_url, headers=headers, verify=False)

    if response.status_code == 200:
        return response.json()

    print(f"Failed to fetch issue: {response.status_code} - {response.text}")
    return None

def get_user_info(access_token):
    """Get the current user's information from Jira."""
    base_url = settings.jira_url.rstrip('/')
    user_url = f"{base_url}/rest/api/latest/myself"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(user_url, headers=headers, verify=False)
        if response.status_code == 200:
            user_data = response.json()
            return {
                "name": user_data.get("displayName", ""),
                "email": user_data.get("emailAddress", ""),
                "accountId": user_data.get("accountId", "")
            }
        else:
            print(f"Failed to get user info: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error getting user info: {str(e)}")
        return None