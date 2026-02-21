from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "publisher_date": "2008-08-01",
        "page_count": "464",
        "language": "English",
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt and David Thomas",
        "publisher": "Addison-Wesley",
        "publisher_date": "1999-10-30",
        "page_count": "352",
        "language": "English",
    },
    {
        "id": 3,
        "title": "Refactoring: Improving the Design of Existing Code",
        "author": "Martin Fowler",
        "publisher": "Addison-Wesley Professional",
        "publisher_date": "2018-11-20",
        "page_count": "448",
        "language": "English",
    },
    {
        "id": 4,
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
        "publisher": "Addison-Wesley Professional",
        "publisher_date": "1994-10-31",
        "page_count": "395",
        "language": "English",
    },
    {
        "id": 5,
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "publisher": "MIT Press",
        "publisher_date": "2009-07-31",
        "page_count": "1312",
        "language": "English",
    },
]



# Request/Response model
class RequestModel(BaseModel):
    id: int
    title: str
    author: str


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    publisher_date: date
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title: str
    publisher: str
    page_count: int
    language: str


# ✅ HOME PAGE
@app.get("/")
async def get_books():
    return {"message": "FastAPI running on Kubernetes 🚀"}

# ✅ READ ALL
@app.get("/books", response_model=List[Book])
async def get_books():
    return books


# ✅ READ ONE
@app.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


# ✅ CREATE
@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:
    
    dict_book = book_data.model_dump()
    new_book = {**dict_book}

    books.append(new_book)
    return new_book


# ✅ UPDATE
@app.put("/books/{book_id}")
async def update_book(book_id: int, request: RequestModel):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books[index] = request.model_dump()
            return books[index]
    raise HTTPException(status_code=404, detail="Book not found")


# ✅ DELETE
@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
        
    raise HTTPException(status_code=404, detail="Book not found")


# ✅ PATCH (partial update)
@app.patch("/book/{book_id}")
async def patch_book(book_id: int, book_update: BookUpdateModel) -> dict:
    for book in books:
        if book["id"] == book_id:

            book["title"] = book_update.title
            book["publisher"] = book_update.publisher
            book["page_count"] = book_update.page_count 
            book["language"] = book_update.language

            return book
        
    raise HTTPException(status_code=404, detail="Book not found")
