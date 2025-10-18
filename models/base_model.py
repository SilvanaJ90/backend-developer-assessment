#!/usr/bin/env python3
"""
BaseModel: declarative Base + mixin-like base class.
Defines a single Base instance used by all models.
"""

from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """BaseModel with common columns and helpers."""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize the BaseModel with sensible defaults."""
        # ⚙️ Importante: No romper el constructor de SQLAlchemy
        super().__init__(*args, **kwargs)

        # Asegura siempre un ID único (UUID4)
        if not getattr(self, "id", None):
            self.id = str(uuid.uuid4())

        # Manejo de timestamps
        now = datetime.utcnow()
        if not getattr(self, "created_at", None):
            self.created_at = kwargs.get("created_at", now)
        if not getattr(self, "updated_at", None):
            self.updated_at = kwargs.get("updated_at", now)

    def save(self):
        """Persist the instance using models.storage (lazy import)."""
        from models import storage
        storage.new(self)
        storage.save()

    def delete(self):
        """Delete instance from storage."""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Convert SQLAlchemy model to dictionary."""
        d = dict(self.__dict__)
        d.pop("_sa_instance_state", None)
        d["__class__"] = self.__class__.__name__

        if isinstance(self.created_at, datetime):
            d["created_at"] = self.created_at.strftime(TIME_FORMAT)
        if isinstance(self.updated_at, datetime):
            d["updated_at"] = self.updated_at.strftime(TIME_FORMAT)

        return d

    def __repr__(self):
        """Readable object representation."""
        return f"[{self.__class__.__name__}] ({self.id})"
