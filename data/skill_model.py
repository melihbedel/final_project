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

