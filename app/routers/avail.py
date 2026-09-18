import uuid
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import exc
from app.internal.avail import get_availibity
from app.core.logger import logger
from app.core.database import get_session
from app.core.utils import get_current_user
from app.schemas.meeting_schema import MeetingProposal

TIME_HORIZON = 5
router = APIRouter(prefix='/avail',
                   tags=['avail'])

@router.post('/meeting-propose')
async def propose_meeting(meeting_proposal: MeetingProposal,
                          user_id: uuid.UUID = Depends(get_current_user),
                          session = Depends(get_session)):
    avail_periods = []
    participants = meeting_proposal.participants
    meeting_date = meeting_proposal.meeting_date
    for participant in participants:
        avail_period = get_availibity(username=participant,
                                      meeting_date=meeting_date,
                                      session=session)
        avail_periods.append(avail_period)
    
    
