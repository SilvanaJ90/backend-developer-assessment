#!/usr/bin/env python3
"""
DBStorage: database engine + session management for SQLite (default).
Keeps a single engine instance and a scoped session.
Provides basic CRUD operations for SQLAlchemy models.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from models.base_model import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chat.db")


class DBStorage:
    """Manages the database connection using SQLAlchemy."""

    __engine = None
    __session = None

    def __init__(self, url: str | None = None):
        """Initialize SQLAlchemy engine."""
        url = url or DATABASE_URL
        self.__engine = create_engine(url, echo=False, future=True)

    def reload(self):
        """Create all tables and initialize session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    @property
    def session(self):
        """Return the current session."""
        return self.__session

    def new(self, obj):
        """Add object to session."""
        if self.__session is None:
            self.reload()
        self.__session.add(obj)

    def save(self):
        """Commit session."""
        try:
            self.__session.commit()
        except SQLAlchemyError:
            self.__session.rollback()
            raise

    def delete(self, obj):
        """Delete object from session."""
        if self.__session is None:
            self.reload()
        self.__session.delete(obj)
        self.__session.commit()

    def all(self, cls=None):
        """Return all objects of a class."""
        if self.__session is None:
            self.reload()
        result = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{getattr(obj, 'id', '')}"
                result[key] = obj
        return result

    def get(self, cls, id):
        """Return object by id."""
        if self.__session is None:
            self.reload()
        return self.__session.query(cls).filter_by(id=id).first()

    def close(self):
        """Close the session."""
        if self.__session:
            self.__session.remove()
