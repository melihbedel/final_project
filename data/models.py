from pydantic import BaseModel


class Professional(BaseModel):
    id: int or None = None
    first_name: str
    last_name: str
    login_id2: int


class RegisterDataProfessional(BaseModel):
    id: int or None = None
    username: str
    password: str
    first_name: str
    last_name: str
    type: int = 0


class ProfessionalInfo(BaseModel):
    id: int or None = None
    summary: str
    location: str
    status: int
    logo: str


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


class CompanyAds(BaseModel):
    id: int or None = None
    salary_min: int
    salary_max: int
    description: str
    location: str
    status: str

    @classmethod
    def from_query_result(cls, id, company_id, salary_min, salary_max, description, location, status):
        return cls(
            id=id,
            company_id=company_id,
            salary_min=salary_min,
            salary_max=salary_max,
            description=description,
            location=location,
            status=status
        )