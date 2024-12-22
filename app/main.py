from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import books
import time
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()  # Load variables from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

class SuggestionRequest(BaseModel):
    author: str

@app.post("/suggestion")
async def get_book_suggestions(request: SuggestionRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are helpful assistant that suggests books based on an author's name",
                },
                {
                    "role": "user",
                    "content": f"Suggest 2-3 books written by {request.author}.",
                },
            ],
            max_tokens=100,
            temperature=0.7,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching suggestions: {str(e)}")
    finally:
        print("BUON NATALE")
    
    suggestions = response.choices[0].message.content.strip().split("\n")
    return {
        "author": request.author,
        "suggestions": suggestions
    }



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.middleware("http")
async def add_custom_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)  # Call the next middleware or route
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routers
app.include_router(books.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to my TBR"}
