from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import books
import time

app = FastAPI()

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
