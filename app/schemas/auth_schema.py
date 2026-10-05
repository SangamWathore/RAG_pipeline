from pydantic import BaseModel, ConfigDict

class RegisterRequest(BaseModel):
    username : str
    password : str

class UserResponse(BaseModel):
    id:int
    username:str

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):

    username: str
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str
