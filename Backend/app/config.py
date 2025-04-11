from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Jira OAuth settings
    jira_oauth_client_id: str = os.getenv("JIRA_OAUTH_CLIENT_ID", "")
    jira_oauth_client_secret: str = os.getenv("JIRA_OAUTH_CLIENT_SECRET", "")
    jira_oauth_auth_url: str = os.getenv("JIRA_OAUTH_AUTH_URL", "https://127.0.0.1:8443/rest/oauth2/latest/authorize")
    jira_oauth_token_url: str = os.getenv("JIRA_OAUTH_TOKEN_URL", "https://127.0.0.1:8443/rest/oauth2/latest/token")
    jira_oauth_redirect_uri: str = os.getenv("JIRA_OAUTH_REDIRECT_URI", "https://local.myapp.com:3000/auth/callback")
    
    # Jira API settings
    jira_url: str = os.getenv("JIRA_URL", "https://127.0.0.1:8443")
    
    # Frontend URL
    frontend_url: str = os.getenv("FRONTEND_URL", "https://local.myapp.com:3000")

    # Database settings
    database_url: str = os.getenv("DATABASE_URL")
    database_echo: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
