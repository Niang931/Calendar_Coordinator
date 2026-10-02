import uuid
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import  Mapped, relationship, mapped_column
from datetime import date, time, datetime
from sqlalchemy import JSON
from app.core.database import Base

    
class Task(Base):
    
    __tablename__ = 'tasks'
    task_id : Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                          server_default=text('gen_random_uuid()'))
    title : Mapped[str] = mapped_column()
    start_date : Mapped[date] = mapped_column()
    start_time: Mapped[time] = mapped_column()
    duration : Mapped[float] = mapped_column()
    user_schedules = relationship(
        'User_Schedule',
        back_populates="task",
        cascade='all, delete-orphan'
    )


class User_Schedule(Base):
    
    __tablename__ = 'user_schedule'
    us_id : Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                              server_default=text('gen_random_uuid()'))
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey('users.user_id',
                                                           ondelete='CASCADE'),
                                                nullable=False)
    task_id : Mapped[uuid.UUID] = mapped_column(ForeignKey('tasks.task_id',
                                                           ondelete='CASCADE'),
                                                nullable=False)
    created_at: Mapped[date] = mapped_column(server_default=text('current_date')) 
    task = relationship(
        "Task",
        back_populates='user_schedules'
    )
    user = relationship(
        'User',
        back_populates='user_schedules'
    )

    


    
