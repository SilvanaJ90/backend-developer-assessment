#!/usr/bin/python3
"""Message model"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base_model import BaseModel, Base

class Message(BaseModel, Base):
    __tablename__ = "messages"

    session_id = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    content = Column(String(512), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="messages")
