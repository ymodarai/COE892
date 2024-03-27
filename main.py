#run uvicorn main:app --reload 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin, you should limit this to specific origins in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allowed HTTP methods
    allow_headers=["*"],  # Allowed headers, you may restrict this based on your needs
)

class Book(BaseModel):
    title: str
    author: str
    image_url: str

books = [
    Book(title="Harry Potter and the Philosopher's Stone", author="J.K. Rowling", image_url="https://m.media-amazon.com/images/I/91wKDODkgWL._AC_UF1000,1000_QL80_.jpg"),
    Book(title="The Fault in our Stars", author="John Green", image_url="https://m.media-amazon.com/images/I/61fbVx3W5cL._AC_UF1000,1000_QL80_.jpg"),
    Book(title="Paper Towns", author="John Green", image_url="https://m.media-amazon.com/images/I/81245cfOyCL._AC_UF350,350_QL50_.jpg")
]

@app.get("/books", response_model=List[Book])
async def get_books():
    return books


