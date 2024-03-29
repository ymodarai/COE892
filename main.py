#run uvicorn main:app --reload 

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

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
    is_taken: bool = False
    borrower_username: Optional[str] = None

books = [
    Book(title="Harry Potter and the Philosopher's Stone", author="J.K. Rowling", image_url="https://m.media-amazon.com/images/I/91wKDODkgWL._AC_UF1000,1000_QL80_.jpg"),
    Book(title="The Fault in our Stars", author="John Green", image_url="https://m.media-amazon.com/images/I/61fbVx3W5cL._AC_UF1000,1000_QL80_.jpg"),
    Book(title="Paper Towns", author="John Green", image_url="https://m.media-amazon.com/images/I/81245cfOyCL._AC_UF350,350_QL50_.jpg")
]

@app.get("/books", response_model=List[Book])
async def get_books():
    return [book for book in books if not book.is_taken]

def get_book_by_title(title: str) -> Book:
    for book in books:
        if book.title == title:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books")
async def update_book_status(title: str = Body(...), is_taken: bool = Body(...), borrower_username: Optional[str] = Body(None)):
    for book in books:
        if book.title == title:
            book.is_taken = is_taken
            book.borrower_username = borrower_username
            return {"message": "Book status updated successfully"}
    return {"error": "Book not found"}


@app.post("/add_book")
async def add_book(book: Book = Body(...)):
    books.append(book)
    return {"message": "Book added successfully", "book": book}

@app.get("/all_books")
async def get_all_books():
    return books

class User(BaseModel):
    username: str
    password: str
    is_librarian: bool

users = [
    User(username="user1", password="password1", is_librarian=True),
    User(username="user2", password="password2", is_librarian=False),
    # Add more users as needed
]

@app.post("/add_user", status_code=201)
async def add_user(user: User):
    users.append(user)
    print(user)
    return {"message": "User added successfully"}

@app.post("/login")
async def login(username: str = Body(...), password: str = Body(...)):
    for user in users:
        if user.username == username:
            if user.password == password:
                return {"message": "Login successful", "is_librarian": user.is_librarian}
            else:
                raise HTTPException(status_code=401, detail="Incorrect password")
    raise HTTPException(status_code=404, detail="User not found")


