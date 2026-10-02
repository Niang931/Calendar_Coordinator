import uuid
from fastapi import APIRouter, HTTPException
from datetime import timedelta, date, time
from fastapi.params import Depends
from sqlalchemy import exc
# from app.models.meeting_model import Meeting_Proposal, Option, Vote
from app.internal.avail import get_availibity, intersect_windows, validate_windows, get_work_date, get_options, add_proposal, add_option
from app.core.database import get_session
from app.core.utils import get_current_user
from app.internal.user import get_user_id
from app.internal.task import filter_task
from app.internal.group import get_group_id, get_user_in_group
from app.schemas.meeting_schema import TimeSlotCheck, TimeSlotProposal


router = APIRouter(prefix='/avail',
                   tags=['avail'])

@router.post('/get-avail')
async def get_availability_on_date(meeting_proposal: TimeSlotCheck,
                          created_at: date = None,
                          user_id: uuid.UUID = Depends(get_current_user),
                          session = Depends(get_session)):
    avail_periods = []
    group_name = meeting_proposal.group_name
    group_id = get_group_id(group_name=group_name, created_at=created_at, session=session)
    if not group_id:
        raise HTTPException(status_code=404, detail='Group not found')
    participants = get_user_in_group(group_id=group_id, session=session)
    meeting_date = meeting_proposal.meeting_date
    for participant in participants:
        tasks = filter_task(user_id=participant, start_date=meeting_date, session=session)
        if tasks:
            avail_period = get_availibity(meeting_date=meeting_date,
                                        tasks=tasks)
            avail_periods.append(avail_period)
        else:
            start_work, end_work = get_work_date(start_date=meeting_date)
            avail_periods.append([(start_work, end_work)])

    if avail_periods:
        current_window = avail_periods[0]

        for i in range(1, len(avail_periods)):
            current_window = intersect_windows(avail_period1=current_window,
                                            avail_period2=avail_periods[i])

        validated_windows = validate_windows(possible_candidates=current_window,
                                            meeting_duration=timedelta(hours=meeting_proposal.meeting_duration))
    
    return validated_windows

@router.post('/propose-meeting')
async def propose_meeting(timeslot_proposal: TimeSlotProposal,
                          user_id=Depends(get_current_user),
                          session=Depends(get_session)):
    group_name = timeslot_proposal.group_name
    group_id= get_group_id(group_name=group_name, session=session)
    if not group_id:
        raise HTTPException(status_code=404, detail='Group not found')
    add_proposal(timeslot_proposal=timeslot_proposal, session=session)
    return 'succeed'

@router.get('/status')
async def check_status(group_name: str,
                       user_id=Depends(get_current_user),
                       session=Depends(get_session)):
    group_id = get_group_id(group_name=group_name, session=session)
    options = get_options(group_id=group_id, session=session)
    
    return options 
    
    
@router.post('/accept')
async def accept(new_proposal: TimeSlotProposal,
                 user_id=Depends(get_current_user),
                 session=Depends(get_session)):
    add_option(timeslot_proposal=new_proposal, session=session)
    





    
