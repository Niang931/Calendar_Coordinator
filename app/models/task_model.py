from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import  Mapped, relationship, mapped_column
from datetime import date, time
import uuid
from app.core.database import Base

    
class Task(Base):
    
    __tablename__ = 'tasks'
    task_id : Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                          server_default=text('gen_random_uuid()'))
    title : Mapped[str] = mapped_column()
    start_date : Mapped[date] = mapped_column()
    start_time: Mapped[time] = mapped_column()
    duration : Mapped[float] = mapped_column()
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'),
                                                nullable=False)
    participants: Mapped[list["Association"]] = relationship(back_populates="task")

class Association(Base):
    
    __tablename__ = 'association_table'
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey('users.user_id',
                                                           ondelete='CASCADE'),
                                                nullable=False,
                                                primary_key=True)
    task_id : Mapped[uuid.UUID] = mapped_column(ForeignKey('tasks.task_id',
                                                           ondelete='CASCADE'),
                                                nullable=False,
                                                primary_key=True)
    role : Mapped[str] = mapped_column()
    task: Mapped[list["Task"]] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship(back_populates="task_links")