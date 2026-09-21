"""
Module for Pydantic models for data validation
"""
from pydantic import BaseModel, Field  # We can enforce attribute values with Field


class Book(BaseModel):
    # The ellipses is a sentinel value meaning "this field is required / no default values"
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., gt=1900,lt=2100)


class UserBody(BaseModel):
    name: str
    email: str
