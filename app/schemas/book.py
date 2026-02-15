from pydantic import BaseModel
from typing import Optional

class BookOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    tags: Optional[str]

    class Config:
        from_attributes = True
