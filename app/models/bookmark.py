from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    page_number = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="unique_user_book"),
    )

    user = relationship("User", back_populates="bookmarks")
    book = relationship("Book", back_populates="bookmarks")

