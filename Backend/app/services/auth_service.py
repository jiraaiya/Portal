import requests
from app.config import settings

def authenticate_user(credentials):
    """Authenticate the user with Jira API using Bearer Token."""
    # Construct Jira API URL for authentication
    jira_url = f"{settings.jira_url}/rest/api/2/myself"
    
    # Prepare the headers to use Bearer token
    headers = {
        "Authorization": f"Bearer {credentials.api_token}",
        "Accept": "application/json"
    }

    # Send the GET request to Jira API to authenticate
    response = requests.get(jira_url, headers=headers)

    # Debugging the response status and content
    print(f"Jira API response: {response.status_code} {response.text}")

    # Check if the response was successful
    if response.status_code == 200:
        return True
    return False
