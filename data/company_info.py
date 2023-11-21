from pydantic import BaseModel


class CompanyInfo(BaseModel):
    id: int or None = None
    description: str
    location: str
    contacts: str
    logo: str
    job_ads: int or None = None  # number of active jobs!!!!
    matches: int or None = None  # number of matches!!!!


class CompanyInfoForEdit(BaseModel):
    id: int or None = None
    description: str
    location: str
    contacts: str
    logo: str

    @classmethod
    def from_query_result1(cls, id, description, location, contacts, logo, job_ads, matches):
        return cls(
            id=id,
            description=description,
            location=location,
            contacts=contacts,
            logo=logo,
            job_ads=job_ads,
            matches=matches
        )
