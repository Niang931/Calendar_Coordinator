import uuid
import operator
from datetime import date, timedelta, datetime, time
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.internal.task import filter_task
from app.internal.user import get_user_id_by_username
from app.models.task_model import Task

START_WORK = time(6, 0)
END_WORK = time(22, 0)
interval = tuple[datetime, datetime]

def get_work_date(tasks: list[Task]) -> date:
    start_date = tasks[0].start_date
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

def get_availibity(username: str, meeting_date: date, session: Session) -> list[interval]:
    user_id = get_user_id_by_username(username=username, session=session)
    tasks = filter_task(user_id=user_id, session=session, start_date=meeting_date)
    if tasks:
        start_work, end_work = get_work_date(tasks=tasks)
        busy_period = get_busy_period(tasks=tasks)
        if busy_period:
            avail_period = get_avail_period(busy_period=busy_period,
                                            start_work=start_work,
                                            end_work=end_work)
            return avail_period
        return [(start_work, end_work)]


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


