from pydantic import BaseModel
from enum import Enum


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


class JobAdsReturn(BaseModel):
    id: int or None = None
    salary_min: int
    salary_max: int
    description: str
    location: str
    status: str = 'Active'


class JobAds(BaseModel):
    id: int or None = None
    salary_min: int
    salary_max: int
    description: str
    location: str
    status: int


class JobAdsReturn(BaseModel):
    id: int or None = None
    salary_min: int
    salary_max: int
    description: str
    location: str



    @classmethod
    def from_query_result1(cls, id, company_id, salary_min, salary_max, description, location, status):
        return cls(
            id=id,
            company_id=company_id,
            salary_min=salary_min,
            salary_max=salary_max,
            description=description,
            location=location,
            status=status
        )


class Status(str, Enum):
    active = "Active"
    archived = "Archived"
