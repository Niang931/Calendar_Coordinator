from sqlalchemy import ForeignKey, String, Integer, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                     server_default=text("gen_random_uuid()"))
    username: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    