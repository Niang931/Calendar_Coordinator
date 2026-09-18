from sqlalchemy import ForeignKey, String, Integer, Table, Column, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date, time
import uuid
from app.models.user_model import User
from app.core.database import Base

association_table = Table(
    'association_table',
    Base.metadata,
    Column('user_id', ForeignKey('users.user_id')),
    Column('meeting_id', ForeignKey('tasks.task_id'))
)
    
class Task(Base):
    
    __tablename__ = 'tasks'
    task_id : Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                          server_default=text('gen_random_uuid()'))
    title : Mapped[str] = mapped_column()
    start_date : Mapped[date] = mapped_column()
    start_time: Mapped[time] = mapped_column()
    duration : Mapped[float] = mapped_column()
    participants: Mapped[list[User]]= relationship(secondary=association_table)
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'),
                                                nullable=False)