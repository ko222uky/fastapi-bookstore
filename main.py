from fastapi import FastAPI

#----------------------------------------------
from models import Book # example Pydantic model
#----------------------------------------------

#----------------------------------------------
from pydantic import BaseModel # for example of managing response formats
from typing import Any
#----------------------------------------------

#----------------------------------------------
# Error handling - basic HTTP error
from fastapi import HTTPException
from starlette.responses import JSONResponse
#----------------------------------------------

#----------------------------------------------
# Error handling - data validation errors
import json
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
#----------------------------------------------

#############################
# Main app instantiated
app = FastAPI()
#############################

# Root endpoint. Maybe redirect from here
@app.get("/")
async def read_root():
    return {"Hello" : "World"}

# Example for custom exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "Oops! Something went wrong. What happened?!"
        }
    )

# Endpoint to test errors
@app.get("/error_endpoint")
async def raise_exception():
    raise HTTPException(status_code=400)

# Example of custom responses for data validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return PlainTextResponse(
        "This is a plain text response:"
        f" \n{json.dumps(exc.errors(), indent=2)}",
        status_code=status.HTTP_404_NOT_FOUND
    )

# Example for managing response formats with pydantic
class BookResponse(BaseModel):
    """Custom response using BaseModel."""
    title: str
    author: str

@app.get("/allbooks", response_model=list[BookResponse])
async def read_all_books() -> Any: # we specify response_model in decorator, instead of returning -> list[BookResponse]
    """Endpoint to demonstrate custom response formats
    using Pydantic."""
    return [
        {
            "id": 1,
            "title": "1984",
            "author": "George Orwell"
        },

        {
            "id": 1,
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald"
        }
    ]

# Example POST with data simple pydantic validation
@app.post("/book")
async def create_book(book: Book):
    return book

# Examples of endpoints using path parameters
@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {
        "book_id" : book_id,
        "title" : "The Great Gatsby",
        "author" : "F. Scott Fitzgerald"
    }

@app.get("/authors/{author_id}")
async def read_author(author_id: int):
    return {
        "author_id": author_id,
        "name": "Ernest Hemingway"
    }


