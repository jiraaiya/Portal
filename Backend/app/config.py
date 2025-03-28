from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    jira_url: str
    jira_user: str
    jira_api_token: str

    class Config:
        env_file = Path(__file__).parent.parent / ".env"

settings = Settings()

# Debugging: Print out values to check if .env is loaded correctly
print(f"Jira URL: {settings.jira_url}")
print(f"Jira User: {settings.jira_user}")
print(f"Jira API Token: {settings.jira_api_token}")
