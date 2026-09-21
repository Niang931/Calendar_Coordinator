import uuid
from fastapi import APIRouter
from datetime import timedelta
from fastapi.params import Depends
from sqlalchemy import exc
from app.internal.avail import get_availibity, intersect_windows, validate_windows
from app.core.database import get_session
from app.core.utils import get_current_user
from app.schemas.meeting_schema import MeetingProposal

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

    current_window = intersect_windows(avail_period1=avail_periods[0],
                                       avail_period2=avail_periods[1])
    print(current_window)
    for i in range(2, len(avail_periods)):
        current_window = intersect_windows(avail_period1=current_window,
                                           avail_period2=avail_periods[i])

    validated_windows = validate_windows(possible_candidates=current_window,
                                         meeting_duration=timedelta(hours=meeting_proposal.meeting_duration))
    return validated_windows




    
