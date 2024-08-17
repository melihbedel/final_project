from pydantic import BaseModel, constr
from models.skill import Skill
from enum import Enum


class Status(str, Enum):
    ACTIVE = 'active'
    ARCHIVED = 'archived'


class JobAd(BaseModel):
    id: int | None = None
    company_id: int | None
    salary_min: int | None
    salary_max: int | None
    description: constr(min_length=1, max_length=200) | None
    location: str | None
    status: str | None
    requirements: list[Skill] = []
    match_requests: dict[str, list] | None


    @classmethod
    def from_database(cls, id, company_id, salary_min, salary_max, description, location, status, requirements: list, match_requests: dict):
        
        return cls(
                    id = id,
                    company_id=company_id,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    description=description,
                    location=location,
                    status=status,
                    requirements=requirements,
                    match_requests=match_requests
        )


class PublicJobAd(BaseModel):
    id: int | None = None
    company_id: int | None
    salary_min: int | None
    salary_max: int | None
    description: constr(min_length=1, max_length=200) | None
    location: str | None
    status: str | None
    requirements: list[Skill] = []

    @classmethod
    def from_jobad(cls, jobad:JobAd):
        return cls(
                    id = jobad.id,
                    company_id=jobad.company_id,
                    salary_min=jobad.salary_min,
                    salary_max=jobad.salary_max,
                    description=jobad.description,
                    location=jobad.location,
                    status=jobad.status,
                    requirements=jobad.requirements
        )


class DataJobAd(BaseModel):
    salary_min: int | None = None
    salary_max: int | None = None
    description: constr(min_length=1, max_length=200) | None = None
    location: str | None = None
    requirements: dict | None = None