from fastapi import APIRouter, HTTPException
from app.database import books_collection
from app.schemas import Book, BookImport
from bson import ObjectId
from typing import List

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

# Helper to convert MongoDB document to Pydantic model
def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]), 
        "Book_Id": book["id"],  
        "Title": book["title"],
        "Author": book["author"],
        "ISBN": book.get("isbn", ""),
        "ISBN13": book.get("isbn13", ""),
        "My_Rating": book.get("my_rating", ""),
        "Average_Rating": book.get("average_rating", ""),
        "Publisher": book.get("publisher", ""),
        "Binding": book.get("binding", ""),
        "Number_of_Pages": book.get("number_of_pages", ""),  
        "Year_Published": book.get("year_published", ""),
        "Original_Publication_Year": book.get("original_publication_year", ""),
        "Data_Read": book.get("data_read", ""),
        "Data_Added": book.get("data_added", ""),
        "Bookshelf": book.get("bookshelf", ""),
        "Bookshelf_w_position": book.get("bookshelf_w_position", ""),
        "Exclusive_Shelf": book.get("exclusive_shelf", False),
        "My_Review": book.get("my_review", ""),
        "Read_Count": book.get("read_count", ""),
        "Owned_copies": book.get("owned_copies", ""),
    }

@router.get("/", response_model=List[Book])
async def get_books():
    """Retrieve all books."""
    books = await books_collection.find().to_list(1000)
    return books

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str):
    """Retrieve a book by ID."""
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if book:
        return book_helper(book)
    raise HTTPException(status_code=404, detail="Book not found")

@router.post("/", response_model=Book)
async def create_book(book: Book):
    """Create a new book."""
    new_book = await books_collection.insert_one(book.dict())
    created_book = await books_collection.find_one({"_id": new_book.inserted_id})
    return book_helper(created_book)

@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: str, updated_book: Book):
    """Update an existing book."""
    result = await books_collection.update_one(
        {"_id": ObjectId(book_id)}, {"$set": updated_book.dict()}
    )
    if result.modified_count == 1:
        updated = await books_collection.find_one({"_id": ObjectId(book_id)})
        return book_helper(updated)
    raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/{book_id}", response_model=dict)
async def delete_book(book_id: str):
    """Delete a book."""
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

# Import books from a JSON array
@router.post("/import", response_model=dict)
async def import_books(data: List[BookImport]):
    """Import books from a JSON array."""
    imported_books = []
    
    # Iterate through each book data in the incoming list
    for book_data in data:
        # Map fields from BookImport to Book
        book = Book(
            id=str(book_data.Book_Id),  # MongoDB _id should be string
            title=book_data.Title,
            author=book_data.Author,
            second_author=book_data.Second_Author,
            my_rating=book_data.My_Rating,
            publisher=book_data.Publisher,
            binding=book_data.Binding,
            num_pages=book_data.Number_of_Pages,
            publication_year=book_data.Original_Publication_Year,
            bookshelf=book_data.Bookshelf,
            copies=book_data.Owned_Copies,
            read=book_data.Exclusive_Shelf == "read",
            
        )

        # Check if the book already exists in the MongoDB collection
        existing_book = await books_collection.find_one({"id": book.id})
        if existing_book:
            raise HTTPException(
                status_code=400,
                detail=f"Book with ID {book.id} already exists"
            )
        
        # Insert the new book into MongoDB
        await books_collection.insert_one(book.dict())
        imported_books.append(book)

    return {"message": f"{len(imported_books)} books imported successfully."}
