from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: Optional[str] = None  # MongoDB ObjectId as a string
    title: str
    author: str
    read: bool = False

class BookImport(BaseModel):
    Book_Id: str
    Title: str 
    Author: str
    Second_Author: Optional[str] = None
    Additional_Author: Optional[str] = None
    ISBN: Optional[str] = None
    ISBN13: Optional[str] = None
    My_Rating:  Optional[str] = None
    Average_Rating: Optional[str] = None
    Publisher:  Optional[str] = None
    Binding: Optional[str] = None
    Number_of_Pages:  Optional[str] = None
    Year_Published: Optional[str] = None
    Original_Publication_Year: str
    Date_Read: Optional[str] = None
    Data_Added:  Optional[str] = None
    Bookshelf:  Optional[str] = None
    Bookshelves_w_positions:  Optional[str] = None
    Exclusive_Shelf:  Optional[str] = None
    My_Review: Optional[str] = None
    Read_Count:  Optional[str] = None
    Owned_Copies:  Optional[str] = None