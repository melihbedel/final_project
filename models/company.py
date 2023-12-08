from pydantic import BaseModel

class Company(BaseModel):
    id: int
    name: str
    description: str | None
    location: str | None
    contacts: str | None
    active_ads: int | None
    matches: int | None
    # logo: bytes

    @classmethod
    def from_database(cls, id, name, description=None, location=None, contacts=None, active_ads=None, matches=None):

        return cls(
            id=id,
            name=name,
            description=description,
            location=location,
            contacts=contacts,
            active_ads=active_ads,
            matches=matches
        )
    

class RegisterDataCompany(BaseModel):
    username: str
    password: str
    name: str

class EditCompany(BaseModel):
    name: str | None = None
    description: str | None = None
    location: str | None = None
    contacts: str | None = None