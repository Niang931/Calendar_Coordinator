import uuid
import operator
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.internal.task import filter_task
from app.internal.user import get_user_id_by_username
from app.models.task_model import Task

START_WORK = 6
END_WORK = 22

def get_busy_period(tasks: list[Task]) -> list[tuple]:
    '''Compute busy period for one day'''
    busy_period = []
    for task in tasks:
        start_time = task.start_time
        end_time = start_time + timedelta(task.duration)
        busy_period.append(tuple(start_time, end_time))
    busy_period = busy_period.sort(key=operator.itemgetter(0))
    merged = []
    for start, end in busy_period:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0],
                          max(merged[-1][1], end))
    return merged
        
def get_avail_period(busy_period: list[tuple],
                     start_work: int = START_WORK,
                     end_work: int = END_WORK) -> list[tuple]:
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

def intersect_windows(avail_period1: list[tuple],
                      avail_period2: list[tuple]) -> list[tuple]:
    '''Compare the two users' avail windows to see the overlapping free time'''
    intersect = []
    i = 0
    j = 0
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

def validate_windows(possible_candidates: list[tuple],
                     meeting_duration: float) -> list[tuple]:
    '''Ensure that the possible time slots has enough time difference for the meeting'''
    valid_period = []
    for start, end in possible_candidates:
        duration = end - start
        if duration >= meeting_duration:
            valid_period.append((start, end))
    return valid_period

def get_availibity(username: str, meeting_date: date, session: Session):
    user_id = get_user_id_by_username(username=username, session=session)
    tasks = filter_task(user_id=user_id, session=session, date=meeting_date)
    busy_period = get_busy_period(tasks=tasks)
    avail_period = get_avail_period(busy_period=busy_period)
    return avail_period
