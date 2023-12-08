from pydantic import BaseModel

class Level:
    BEGINNER = 'beginner'
    ADVANCED = 'advanced'
    EXPERT = 'expert'
    levels = [BEGINNER, ADVANCED, EXPERT]

class Skill(BaseModel):
    skill: str
    level: str

    @classmethod
    def from_database(cls, skill, level):
        return cls(
            skill=skill,
            level=level
        )

