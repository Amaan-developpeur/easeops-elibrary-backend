from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from app.database import get_db
from app.models.book import Book
from app.schemas.book import BookOut

from app.models.bookmark import Bookmark
from app.core.security import get_current_user
from app.schemas.bookmark import BookmarkCreate, BookmarkOut

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteOut
from app.schemas.api_response import APIResponse



router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=APIResponse[List[BookOut]])
def list_books(
    category: str | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    query = db.query(Book)

    if category:
        query = query.filter(Book.category == category)

    if search:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.description.ilike(f"%{search}%")
            )
        )

    offset = (page - 1) * limit

    books = query.offset(offset).limit(limit).all()

    return {
    "success": True,
    "data": books,
    "message": None
    }


# ----------------------------
from fastapi import HTTPException

@router.get("/{book_id}", response_model=APIResponse[BookOut])
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
    "success": True,
    "data": book,
    "message": None
    }

# ----------------

@router.post("/{book_id}/bookmark", response_model=APIResponse[BookmarkOut])
def add_bookmark(
    book_id: int,
    data: BookmarkCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.book_id == book_id
    ).first()

    if not bookmark:
        bookmark = Bookmark(
            user_id=current_user.id,
            book_id=book_id,
            page_number=data.page_number
        )
        db.add(bookmark)
    else:
        bookmark.page_number = data.page_number

    db.commit()
    db.refresh(bookmark)

    return {
    "success": True,
    "data": bookmark,
    "message": None
    }

# --------------------------
@router.delete("/{book_id}/bookmark", response_model=APIResponse[None])

def remove_bookmark(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.book_id == book_id
    ).first()

    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    db.delete(bookmark)
    db.commit()

    return {
    "success": True,
    "data": None,
    "message": "Bookmark removed"
    }


# ----------------------------------
@router.post("/{book_id}/notes", response_model=APIResponse[NoteOut])
def add_note(
    book_id: int,
    data: NoteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    note = Note(
        user_id=current_user.id,
        book_id=book_id,
        page_number=data.page_number,
        note_text=data.note_text
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return {
    "success": True,
    "data": note,
    "message": None
    }

# ---------
@router.get("/{book_id}/notes", response_model=APIResponse[List[NoteOut]])
def get_notes(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    notes = db.query(Note).filter(
        Note.user_id == current_user.id,
        Note.book_id == book_id
    ).all()

    return {
    "success": True,
    "data": notes,
    "message": None
    }


