from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    email: EmailStr


class UserDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr

    