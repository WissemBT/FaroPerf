from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="User")  # "Admin" or "User"
    created_at = Column(DateTime, default=datetime.utcnow)
    hashed_password = Column(String, nullable=False)

    servers = relationship("Server",  back_populates="owner",
                           cascade="all, delete-orphan", passive_deletes=True)
    notifications = relationship("Notification", back_populates="user",
                                 cascade="all, delete-orphan", passive_deletes=True)

