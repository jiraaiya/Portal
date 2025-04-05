from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    jira_url: str
    jira_user: str
    jira_api_token: str

    # ✅ OAuth 2.0 settings
    jira_oauth_client_id: str
    jira_oauth_client_secret: str
    jira_oauth_redirect_uri: str
    jira_oauth_auth_url: str
    jira_oauth_token_url: str

    class Config:
        env_file = Path(__file__).parent.parent / ".env"

settings = Settings()
