from pydantic import BaseModel

class UserCredentials(BaseModel):
    # username: str
    api_token: str
