from pydantic import BaseModel

class User(BaseModel):
 email: str
 password: str
 password_confirmation: str = None