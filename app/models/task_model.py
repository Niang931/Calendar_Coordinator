from sqlalchemy import ForeignKey, String, Integer, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, date
import uuid
from app.core.database import Base
    
class Task(Base):
    
    __tablename__ = 'tasks'
    task_id : Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                          server_default=text('gen_random_uuid()'))
    title : Mapped[str] = mapped_column()
    deadline : Mapped[datetime] = mapped_column()
    duration : Mapped[float] = mapped_column()
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'),
                                                nullable=False)