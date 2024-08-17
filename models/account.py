from pydantic import BaseModel, constr
from enum import Enum


class Type(str, Enum):
    PROFESSIONAL = 'professional'
    COMPANY = 'company'


class LoginData(BaseModel):
    username: str
    password: str


class Account(BaseModel):
    id: int | None = None
    username: constr(pattern='^\w{2,45}$')
    password: str
    type: str

    @classmethod
    def from_database(cls, id, username, password, type):
        
        return cls(
                    id = id,
                    username=username,
                    password=password,
                    type=type
        )