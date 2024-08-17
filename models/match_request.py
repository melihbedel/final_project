from pydantic import BaseModel
from enum import Enum

class Response(str, Enum):
    ACCEPT = 'accept'
    REJECT = 'reject'

class Status:
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class MatchRequest(BaseModel):
    sender: str
    ad_id: int
    status: str

    @classmethod
    def from_database(cls, sender: str, ad_id: int, status: Status, type):
        return cls(
            sender=f'{type} {sender}',
            ad_id=ad_id,
            status=status
        )