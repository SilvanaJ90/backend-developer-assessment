#!/usr/bin/python3
"""Defines the User model"""

from sqlalchemy import Column, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from models.base_model import Base, BaseModel


class User(BaseModel, Base):
    """Representation of a user"""

    __tablename__ = "users"

    # Campos principales
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    is_user = Column(Boolean, default=True, nullable=False)

    @property
    def password(self):
        """Prevent direct access to password attribute"""
        raise AttributeError("password is not a readable attribute")

    def set_password(self, password: str) -> None:
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Check hashed password"""
        return check_password_hash(self.password_hash, password)

    def __init__(self, *args, **kwargs):
        """Initialize user, ensuring password is hashed"""
        super().__init__(*args, **kwargs)

        # Si viene una contraseña sin hash, la convertimos
        raw_pass = kwargs.get("password")
        if raw_pass and not kwargs.get("password_hash"):
            self.set_password(raw_pass)
