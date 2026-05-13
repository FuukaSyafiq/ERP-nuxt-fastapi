from pydantic import BaseModel

class RegisterDto(BaseModel):
    password: str
    email: str