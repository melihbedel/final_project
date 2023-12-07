from enum import Enum

from pydantic import BaseModel


class SkillLevel(str, Enum):
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'
    MASTER = 'Master'


class CreateSkill(BaseModel):
    skill: str


class DisplaySkill(BaseModel):
    id: int or None = None
    skill: str
    level: str


class IdAndType(BaseModel):
    id: int or None = None
    type: int

    @classmethod
    def from_query_result(cls, id, type):
        return cls(
            id=id,
            type=type,
        )
