from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    category = Column(String, index=True)
    tags = Column(String)  # simple comma-separated for now
    content = Column(Text)  # storing content directly for assignment
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bookmarks = relationship(
    "Bookmark",
    back_populates="book",
    cascade="all, delete-orphan"
    )
