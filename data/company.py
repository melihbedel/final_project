from pydantic import BaseModel


class Company(BaseModel):
    id: int or None = None
    name: str
    login_id1: int


class CompanyInfo(BaseModel):
    id: int or None = None
    description: str
    location: str
    contacts: str
    logo: str
    job_ads: int or None = None  # number of active jobs!!!!
    matches: int or None = None  # number of matches!!!!


class RegisterDataCompany(BaseModel):
    id: int or None = None
    username: str
    password: str
    name: str
    type: int = 1


class CompanyInfoForEdit(BaseModel):
    id: int or None = None
    description: str
    location: str
    contacts: str
    logo: str


class JobAds(BaseModel):
    id: int or None = None
    salary_min: int
    salary_max: int
    description: str
    location: str
    status: int



