from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import requests
from urllib.parse import urlencode
from app.config import settings  # assuming your settings are here
import urllib3
from app.services.jira_service import get_user_info

# Disable SSL verification warnings for local development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

router = APIRouter()

@router.get("/auth/login")
def login_with_jira():
    query = urlencode({
        "response_type": "code",
        "client_id": settings.jira_oauth_client_id,
        "redirect_uri": settings.jira_oauth_redirect_uri,
        "scope": "WRITE"
    })
    print(f"Redirecting to: {settings.jira_oauth_auth_url}?{query}")

    return RedirectResponse(f"{settings.jira_oauth_auth_url}?{query}")


@router.get("/auth/callback")
def jira_auth_callback(request: Request, code: str = None, state: str = None):
    print(f"Auth callback received with code: {code}")
    
    if not code:
        print("No authorization code provided")
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    try:
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.jira_oauth_client_id,
            "client_secret": settings.jira_oauth_client_secret,
            "code": code,
            "redirect_uri": settings.jira_oauth_redirect_uri,
        }
        
        print(f"Token request data: {data}")
        print(f"Token URL: {settings.jira_oauth_token_url}")

        # Disable SSL verification for local development
        token_response = requests.post(
            settings.jira_oauth_token_url, 
            data=data,
            verify=False  # Disable SSL verification
        )

        print(f"Token response status: {token_response.status_code}")
        print(f"Token response headers: {token_response.headers}")
        print(f"Token response body: {token_response.text}")

        if token_response.status_code == 400:
            error_data = token_response.json()
            print(f"Token error: {error_data}")
            if error_data.get("error") == "invalid_grant":
                # If the code was already used, redirect back to login
                print("Invalid grant, redirecting to login")
                return RedirectResponse(url="/auth/login")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch access token: {error_data.get('error_description', 'Unknown error')}"
            )

        if token_response.status_code != 200:
            print(f"Token response error: {token_response.status_code} - {token_response.text}")
            raise HTTPException(
                status_code=token_response.status_code, 
                detail=f"Failed to fetch access token: {token_response.text}"
            )

        token_data = token_response.json()
        print(f"Token data: {token_data}")
        
        # Validate the token by making a request to the Jira API
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="No access token in response")
            
        # Validate the token
        base_url = settings.jira_url.rstrip('/')
        validate_url = f"{base_url}/rest/api/latest/myself"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        print(f"Validating token with URL: {validate_url}")
        print(f"Validation headers: {headers}")
        
        validate_response = requests.get(validate_url, headers=headers, verify=False)
        print(f"Validation response status: {validate_response.status_code}")
        print(f"Validation response headers: {validate_response.headers}")
        print(f"Validation response body: {validate_response.text}")
        
        if validate_response.status_code != 200:
            print(f"Token validation failed: {validate_response.status_code} - {validate_response.text}")
            raise HTTPException(status_code=400, detail="Invalid access token")
            
        print("Token validated successfully")
        
        # Get user information
        user_info = get_user_info(access_token)
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user information")
        
        return {
            "access_token": access_token,
            "expires_in": token_data.get("expires_in"),
            "refresh_token": token_data.get("refresh_token"),
            "scope": token_data.get("scope"),
            "token_type": token_data.get("token_type"),
            "user": user_info
        }
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to communicate with Jira: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.post("/auth/refresh")
async def refresh_token(request: Request):
    """Refresh the access token using the refresh token."""
    try:
        body = await request.json()
        refresh_token = body.get("refresh_token")
        
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token not provided")
        
        data = {
            "grant_type": "refresh_token",
            "client_id": settings.jira_oauth_client_id,
            "client_secret": settings.jira_oauth_client_secret,
            "refresh_token": refresh_token,
        }
        
        # Disable SSL verification for local development
        token_response = requests.post(
            settings.jira_oauth_token_url, 
            data=data,
            verify=False  # Disable SSL verification
        )
        
        if token_response.status_code != 200:
            print(f"Token refresh error: {token_response.status_code} - {token_response.text}")
            raise HTTPException(
                status_code=token_response.status_code, 
                detail=f"Failed to refresh token: {token_response.text}"
            )
        
        token_data = token_response.json()
        return {
            "access_token": token_data.get("access_token"),
            "expires_in": token_data.get("expires_in"),
            "refresh_token": token_data.get("refresh_token"),
            "token_type": token_data.get("token_type")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))