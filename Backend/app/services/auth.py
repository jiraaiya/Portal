from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.config import settings

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.jira_oauth_auth_url,
    tokenUrl=settings.jira_oauth_token_url,
)

async def get_current_user_token(token: str = Depends(oauth2_scheme)):
    """Get the current user's Jira access token."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token