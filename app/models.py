from datetime import datetime
from typing import List, Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # İlişkiler
    projects: Mapped[List["Project"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Project(db.Model):
    __tablename__ = 'projects'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    
    # İlişkiler
    user: Mapped["User"] = relationship(back_populates="projects")
    bug_tickets: Mapped[List["BugTicket"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f'<Project {self.name}>'


class BugTicket(db.Model):
    __tablename__ = 'bug_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='Open')
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=False)
    
    # İlişkiler
    project: Mapped["Project"] = relationship(back_populates="bug_tickets")
    
    def __repr__(self) -> str:
        return f'<BugTicket {self.title}>'
