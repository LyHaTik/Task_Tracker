from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    ForeignKey,
    DateTime,
    func,
    BigInteger
    )
from sqlalchemy.orm import relationship

from app.db.connect import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="user")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    tasks = relationship("Task", back_populates="category")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")


class Setting(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(Boolean, default=True)
