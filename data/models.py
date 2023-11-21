from pydantic import BaseModel


class Company(BaseModel):
    id: int or None = None
    name: str
    login_id1: int





class Professional(BaseModel):
    id: int or None = None
    first_name: str
    last_name: str
    login_id2: int


class RegisterDataCompany(BaseModel):
    id: int or None = None
    username: str
    password: str
    name: str
    type: int = 1


class RegisterDataProfessional(BaseModel):
    id: int or None = None
    username: str
    password: str
    first_name: str
    last_name: str
    type: int = 0


class LoginData(BaseModel):
    id: int or None = None
    username: str
    password: str


class LoginDataForToken(BaseModel):
    id: int or None = None
    username: str
    password: str
    type: int

    @classmethod
    def from_query_result(cls, id, username, password, type):
        return cls(
            id=id,
            username=username,
            password=password,
            type=type
        )


