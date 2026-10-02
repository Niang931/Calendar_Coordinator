import uuid
import operator
from datetime import date, timedelta, datetime, time
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.internal.group import get_group_id, get_user_in_group
from app.internal.task import add_task
from app.models.task_model import Task, User_Schedule
from app.models.group_model import User_Group
from app.models.meeting_model import Meeting_Proposal, Option
from app.schemas.meeting_schema import TimeSlotProposal

START_WORK = time(6, 0)
END_WORK = time(22, 0)
interval = tuple[datetime, datetime]

def get_work_date(start_date: date) -> date:
    start_work = datetime.combine(start_date, START_WORK)
    end_work = datetime.combine(start_date, END_WORK)
    return start_work, end_work

def get_busy_period(tasks: list[Task]) -> list[tuple]:
    '''Compute busy period for one day'''
    busy_period = []
    for task in tasks:
        start_time = datetime.combine(task.start_date, task.start_time)
        end_time = start_time + timedelta(hours=task.duration)
        busy_period.append((start_time, end_time))
    busy_period.sort(key=operator.itemgetter(0))
    merged = []
    if busy_period:
        for start, end in busy_period:
            if not merged or start > merged[-1][1]:
                merged.append((start, end))
            else:
                merged[-1] = (merged[-1][0],
                            max(merged[-1][1], end))
    return merged
        
def get_avail_period(busy_period: list[interval],
                     start_work: datetime,
                     end_work: datetime) -> list[tuple]:
    '''Get empty window by subtracting'''
    ...
    avail_period = []
    current = start_work
    for start, end in busy_period:
        if current < start:
            avail_period.append((current, start))
            
        current = max(current, end)
        
    if current < end_work:
        avail_period.append((current, end_work))
    return avail_period

def get_availibity(meeting_date: date, tasks:list[Task]) -> list[interval]:
    start_work, end_work = get_work_date(start_date=meeting_date)
    busy_period = get_busy_period(tasks=tasks)
    avail_period = get_avail_period(busy_period=busy_period,
                                    start_work=start_work,
                                    end_work=end_work)
    return avail_period


def intersect_windows(avail_period1: list[interval],
                      avail_period2: list[interval]) -> list[interval]:
    '''Compare the two users' avail windows to see the overlapping free time'''
    intersect = []
    i = 0
    j = 0
    if avail_period1 and avail_period2:
        while i < len(avail_period1) and j < len(avail_period2):
            start1, end1 = avail_period1[i]
            start2, end2 = avail_period2[j]
            
            overlap_start = max(start1, start2)
            overlap_end = min(end1, end2)
            if overlap_start < overlap_end:
                intersect.append((overlap_start, overlap_end))
            
            if end1 < end2:
                i += 1
            elif end2 < end1:
                j += 1
            else:
                i += 1
                j += 1
    return intersect


def validate_windows(possible_candidates: list[interval],
                     meeting_duration: timedelta) -> list[interval]:
    '''Ensure that the possible time slots has enough time difference for the meeting'''
    valid_period = []
    for start, end in possible_candidates:
        while (end - start) >= meeting_duration:
            window_end = start + meeting_duration
            valid_period.append((start, window_end))
            start += meeting_duration
    return valid_period

def add_proposal(timeslot_proposal: TimeSlotProposal, 
               session: Session):
    group_name = timeslot_proposal.group_name
    group_id = get_group_id(group_name=group_name, session=session)
    meeting_proposal = Meeting_Proposal(title=timeslot_proposal.title,
                                        group_id=group_id)
    session.add(meeting_proposal)
    option = Option(proposal=meeting_proposal,
                    start_date=timeslot_proposal.meeting_date,
                    start_time=timeslot_proposal.meeting_time,
                    meeting_duration=timeslot_proposal.meeting_duration,
                    description=timeslot_proposal.reason)
    session.add(option)
    
    
def add_option(timeslot_proposal: TimeSlotProposal, session: Session):
    group_name, title = timeslot_proposal.group_name, timeslot_proposal.title
    group_id = get_group_id(group_name=group_name, session=session)
    proposal = session.scalars(select(Meeting_Proposal).where(Meeting_Proposal.group_id==group_id).where(Meeting_Proposal.title==title)).first()
    option = Option(proposal=proposal,
                        start_date=timeslot_proposal.meeting_date,
                        start_time=timeslot_proposal.meeting_time,
                        meeting_duration=timeslot_proposal.meeting_duration,
                        description=timeslot_proposal.reason)
        
    session.add(option) 
    

def get_options(group_id: uuid.UUID, session:Session) -> list[Option]:
    options = []
    proposals = session.scalars(select(Meeting_Proposal).where(Meeting_Proposal.group_id==group_id)).all()
    user_ids = get_user_in_group(group_id=group_id, session=session)
    for proposal in proposals:
        option = session.scalars(select(Option).where(Option.proposal_id==proposal.proposal_id)).all()
        options.append([option])
        if is_all_voted(proposal_id=proposal.proposal_id,
                        group_id=group_id,
                        session=session):
            max_vote = count_max_vote(proposal_id=proposal.proposal_id,
                                      session=session)
            task = Task(title=max_vote.title,
                        start_date=max_vote.start_time,
                        start_time=max_vote.start_date,
                        duration=max_vote.duration)
            session.add(task)
            for user_id in user_ids:
                user_schedule = User_Schedule(user_id=user_id,
                                              task_id=task.task_id)
                session.add(user_schedule)
            
            return max_vote
    return options


def is_all_voted(proposal_id: uuid.UUID, group_id: uuid.UUID, session: Session):
    num_votes = session.query( 
                              func.count(Option.option_id)).where(Option.proposal_id==proposal_id).all()
    num_members = session.query(
                                func.count(User_Group.user_id)).where(User_Group.group_id==group_id).all()
    return num_votes == num_members
    
    
def count_max_vote(proposal_id: uuid.UUID, session: Session):
    stmt = (
    select(
        Option,
        func.count().label("vote_count"),
    )
    .where(Option.proposal_id == proposal_id)
    .group_by(Option.start_time)
    .order_by(func.count().desc())
    .limit(1)
)
    top_option = session.execute(stmt).first()
    return top_option