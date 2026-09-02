from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class Level(Enum):
    low = 1
    medium = 2
    high = 3

class MeetingProposal(BaseModel):
    '''Request to meeting'''
    user_id: str
    meeting_id: str
    participants: list[str]
    acceptable_last_date: datetime
    importance: Level = Level.low
    urgency : Level = Level.low
    candidate: list[Candidate] = []
    state: bool | None = None