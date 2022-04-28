from pydantic import BaseModel
from typing import Optional


class Signup(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_head: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "sam",
                "email": "sam123@gmail.com",
                "password": "password",
                "is_head": False
            }
        }


class TokenData(BaseModel):
    id: Optional[int] = None


class RegisterClub(BaseModel):
    id: Optional[int]
    clubs_registered: Optional[str] = "IIITG"
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "clubs_registered": "DANCE"
            }
        }


class UpdateProfile(BaseModel):
    is_head: Optional[bool] = True

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "is_head": True
            }
        }


class PersonalReminder(BaseModel):
    message: str


class ClubMail(BaseModel):
    message: str
    club: Optional[str] = "IIITG"
