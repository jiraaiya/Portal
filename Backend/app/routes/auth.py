from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import requests
from urllib.parse import urlencode
from app.config import settings  # assuming your settings are here

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
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    data = {
        "grant_type": "authorization_code",
        "client_id": settings.jira_oauth_client_id,
        "client_secret": settings.jira_oauth_client_secret,
        "code": code,
        "redirect_uri": settings.jira_oauth_redirect_uri,
    }

    # Disable SSL verification for local development
    token_response = requests.post(
        settings.jira_oauth_token_url, 
        data=data,
        verify=False  # Disable SSL verification
    )

    if token_response.status_code != 200:
        print(f"Token response error: {token_response.status_code} - {token_response.text}")
        raise HTTPException(
            status_code=token_response.status_code, 
            detail=f"Failed to fetch access token: {token_response.text}"
        )

    token_data = token_response.json()
    return {
        "access_token": token_data.get("access_token"),
        "expires_in": token_data.get("expires_in"),
        "refresh_token": token_data.get("refresh_token"),
        "scope": token_data.get("scope"),
        "token_type": token_data.get("token_type")
    }

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