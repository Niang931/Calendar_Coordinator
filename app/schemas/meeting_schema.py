from pydantic import BaseModel
from datetime import date
from enum import Enum

class Level(Enum):
    low = 1
    medium = 2
    high = 3

class MeetingCandidate(BaseModel):
    ...

class MeetingProposal(BaseModel):
    '''Request to meeting'''
    participants: list[str]
    meeting_date: date
    meeting_duration: float = 1.00
    candidate: list[MeetingCandidate] = []
    state: bool | None = None
    