from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: Optional[str] = None  # MongoDB ObjectId as a string
    title: str
    author: str
    read: bool = False
