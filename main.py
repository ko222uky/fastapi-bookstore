#----------------------------------------------
#----------------------------------------------
# Error handling - data validation errors
import argparse
import json
from typing import Any

#----------------------------------------------
import uvicorn

#----------------------------------------------
# Error handling - basic HTTP error
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

#----------------------------------------------
from sqlalchemy.orm import Session
from fastapi import Depends

#----------------------------------------------
#----------------------------------------------
from pydantic import BaseModel  # for example of managing response formats
from starlette.responses import JSONResponse

#----------------------------------------------
#----------------------------------------------
# router example
import router_example

#----------------------------------------------
from models import Book  # example Pydantic model
from models import UserBody
#----------------------------------------------

# Database sessionn example
from database import SessionLocal, User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#############################
# Main app instantiated
app = FastAPI()

# routers added here:
app.include_router(router_example.router)
#############################

#################################
# Example with users endpoint to get all users
@app.get("/users")
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# example to post a user (add it to db)
@app.post("/user")
def add_new_user(
    user: UserBody, # uses pydantic model
    db: Session = Depends(get_db)
):
    new_user = User( # uses base model which inherits from declarative base from sqlalchemy
        name=user.name,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User).filter(
            User.id == user_id
        ).first()
    )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user
################################








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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default = "localhost", help = "Define the host. E.g., 'localhost' or '0.0.0.0'")
    args = parser.parse_args()
    uvicorn.run('main:app', host = args.host, port=80, reload=True)
