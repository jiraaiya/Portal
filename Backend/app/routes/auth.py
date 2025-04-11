from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from urllib.parse import urlencode
from app.config import settings  # assuming your settings are here
import urllib3
from app.services.jira_service import get_user_info
from pydantic import BaseModel

# Disable SSL verification warnings for local development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

router = APIRouter()

class AuthCallbackRequest(BaseModel):
    code: str

@router.get("/auth/login")
def login_with_jira():
    query = urlencode({
        "response_type": "code",
        "client_id": settings.jira_oauth_client_id,
        "redirect_uri": settings.jira_oauth_redirect_uri,
        "scope": "WRITE"
    })

    return RedirectResponse(f"{settings.jira_oauth_auth_url}?{query}")

@router.post("/auth/callback")
async def jira_auth_callback(request: AuthCallbackRequest):
    if not request.code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    try:
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.jira_oauth_client_id,
            "client_secret": settings.jira_oauth_client_secret,
            "code": request.code,
            "redirect_uri": settings.jira_oauth_redirect_uri,
        }

        # Disable SSL verification for local development
        token_response = requests.post(
            settings.jira_oauth_token_url, 
            data=data,
            verify=False  # Disable SSL verification
        )

        if token_response.status_code == 400:
            error_data = token_response.json()
            if error_data.get("error") == "invalid_grant":
                # If the code was already used, redirect back to login
                return RedirectResponse(url="/auth/login")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch access token: {error_data.get('error_description', 'Unknown error')}"
            )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=token_response.status_code, 
                detail=f"Failed to fetch access token: {token_response.text}"
            )

        token_data = token_response.json()
        
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
        
        validate_response = requests.get(validate_url, headers=headers, verify=False)
        
        if validate_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid access token")
            
        # Get user information
        user_info = get_user_info(access_token)
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user information")
        
        response_data = {
            "access_token": access_token,
            "expires_in": token_data.get("expires_in"),
            "refresh_token": token_data.get("refresh_token"),
            "scope": token_data.get("scope"),
            "token_type": token_data.get("token_type"),
            "user": user_info
        }
        
        return JSONResponse(
            content=response_data,
            headers={
                "Access-Control-Allow-Origin": "https://local.myapp.com:3000",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Accept"
            }
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to communicate with Jira: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.options("/auth/callback")
async def options_callback():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "https://local.myapp.com:3000",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Accept"
        }
    )

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