from pydantic import BaseModel, EmailStr
from typing import List

class Users(BaseModel):
    username : str
    email : str
    project_id : int

class InvitePayload(BaseModel):
    recipient_email : List[EmailStr]
    redoc_link : str
    swagger_link: str
    github_code_link: str