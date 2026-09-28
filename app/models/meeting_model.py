import uuid
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import  Mapped, relationship, mapped_column
from datetime import date, time, datetime
from sqlalchemy import JSON
from app.core.database import Base

class Meeting_Proposal(Base):
    
    __tablename__ = 'meeting_proposals'
    proposal_id: Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                              server_default=text('gen_random_uuid()'))
    title: Mapped[str] = mapped_column()
    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('groups.group_id',
                                                           ondelete='CASCADE'),
                                                nullable=False)
    options = relationship(
        "Option",
        back_populates="proposal",
        cascade="all, delete-orphan"
    )
    
    
class Option(Base):
    
    __tablename__ = 'options'
    option_id: Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                                 server_default=text('gen_random_uuid()'))
    start_date: Mapped[date] = mapped_column()
    start_time: Mapped[time] = mapped_column()
    meeting_duration: Mapped[float] = mapped_column()
    description: Mapped[str] = mapped_column()
    proposal_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('meeting_proposals.proposal_id',
                                                              ondelete='CASCADE'),
                                                   nullable=False)
    proposal = relationship(
        "Meeting_Proposal",
        back_populates='options'
    )
    
class Vote(Base):
    
    __tablename__ = 'votes'
    vote_id: Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                                 server_default=text('gen_random_uuid()'))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'),
                                               nullable=False)
    option_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('options.option_id', ondelete='CASCADE'),
                                                 nullable=False)