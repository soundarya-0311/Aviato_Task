from pydantic import BaseModel

class Users(BaseModel):
    username : str
    email : str
    project_id : int