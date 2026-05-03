from pydantic.networks import EmailStr
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str