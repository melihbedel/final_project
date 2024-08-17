from pydantic import BaseModel

class Status:
    ACTIVE = 'active'
    BUSY = 'busy'

class Professional(BaseModel):
    id: int
    first_name: str
    last_name: str
    summary: str | None
    location: str | None
    status: str | None
    active_ads: int | None
    match_requests: dict[str, list] | None
    # logo: bytes

    @classmethod
    def from_database(cls, id, first_name, last_name, summary=None, location=None, status=None, active_ads=None, match_requests=None):

        return cls(
            id=id,
            first_name=first_name,
            last_name=last_name,
            summary=summary,
            location=location,
            status=status,
            active_ads=active_ads,
            match_requests=match_requests
        )

class RegisterDataProfessional(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

class EditProfessional(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    summary: str | None = None
    location: str | None = None


# def json(self):
#     return {
#         "id": self.id,
#         "name": self.name
#         # Add more attributes as needed