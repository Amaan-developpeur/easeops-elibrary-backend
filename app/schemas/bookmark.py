from pydantic import BaseModel

class BookmarkCreate(BaseModel):
    page_number: int

class BookmarkOut(BaseModel):
    book_id: int
    page_number: int

    class Config:
        from_attributes = True
