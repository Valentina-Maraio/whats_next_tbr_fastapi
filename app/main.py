from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import books_collection
from app.routers.books import router as books_router

import traceback

app = FastAPI()

# Include the books router
app.include_router(books_router)

# Enable CORS for your Vue.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Adjust for your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for suggestion
class SuggestionRequest(BaseModel):
    author: str

@app.post("/suggestion")
async def get_book_suggestions(request: SuggestionRequest):
    """Get book suggestions based on the author."""
    author = request.author
    try:
        # Fetch books by the author from MongoDB
        books = await books_collection.find({"author": author}).to_list(100)
        
        # Extract titles for suggestions
        if books:
            suggestions = [book["title"] for book in books]
        else:
            raise HTTPException(
                status_code=404,
                detail=f"No books found for author '{author}'."
            )
        
        return {
            "author": author,
            "suggestions": suggestions
        }
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An error occurred while fetching book suggestions.")

@app.get("/")
def read_root():
    """Root endpoint for testing."""
    return {"message": "Welcome to the Book Suggestion API"}
