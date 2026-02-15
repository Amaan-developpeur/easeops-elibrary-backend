from pydantic import BaseModel

class NoteCreate(BaseModel):
    page_number: int
    note_text: str

class NoteOut(BaseModel):
    id: int
    page_number: int
    note_text: str

    class Config:
        from_attributes = True
