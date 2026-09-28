import uuid
from app.core.database import Base
from sqlalchemy import text, ForeignKey
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column


class Group(Base):
    
    __tablename__ = 'groups'
    group_id: Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                                server_default=text('gen_random_uuid()'))
    group_name: Mapped[str] = mapped_column()
    group_description: Mapped[str] = mapped_column()

    
class User_Group(Base):
    
    __tablename__ = 'user_group'
    ug_id: Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                             server_default=text('gen_random_uuid()'))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'),
                                               nullable=False)
    group_id : Mapped[uuid.UUID] = mapped_column(ForeignKey('groups.group_id', ondelete='CASCADE'),
                                               nullable=False)
    added_at: Mapped[date] = mapped_column(server_default=text('current_date'))