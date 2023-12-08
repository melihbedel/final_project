from pydantic import BaseModel, constr
from models.skill import Skill

class Status:
    ACTIVE = 'active'
    HIDDEN = 'hidden'
    PRIVATE = 'private'
    MATCHED = 'matched'


class CompanyAd(BaseModel):
    id: int
    professional_id: int
    salary_min: int
    salary_max: int
    description: constr(min_length=1, max_length=200)
    location: str
    status: str
    skillset: list[Skill] = []
    match_requests: dict[str, list] | None

    @classmethod
    def from_database(cls, id, professional_id, salary_min, salary_max, description, location, status, skillset: list, match_requests: dict):
        
        return cls(
                    id=id,
                    professional_id=professional_id,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    description=description,
                    location=location,
                    status=status,
                    skillset=skillset,
                    match_requests=match_requests
        )


class PublicCompanyAd(BaseModel):
    id: int | None = None
    professional_id: int | None
    salary_min: int | None
    salary_max: int | None
    description: constr(min_length=1, max_length=200) | None
    location: str | None
    status: str | None
    skillset: list[Skill] = []

    @classmethod
    def from_companyad(cls, companyad:CompanyAd):
        return cls(
                    id = companyad.id,
                    professional_id=companyad.professional_id,
                    salary_min=companyad.salary_min,
                    salary_max=companyad.salary_max,
                    description=companyad.description,
                    location=companyad.location,
                    status=companyad.status,
                    skillset=companyad.skillset
        )


class DataCompanyAd(BaseModel):
    salary_min: int | None = None
    salary_max: int | None = None
    description: constr(min_length=1, max_length=200) | None = None
    location: str | None = None
    skillset: dict | None = None