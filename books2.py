from fastapi import FastAPI,Body,Path,Query,HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from starlette import status
app=FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: str

    def __init__(self,id,title,author,description,rating,published_date):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.published_date=published_date

# Pydantic is used for validation LIKE adding few rules of the input
# id: Optional[int] = None :::: this means type of id can be int or None
#  model_config ::: this represents the schema which will be visible to the user

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed during creation", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: str = Field(min_length=1, max_length=20)
    model_config={
        "json_schema_extra":{
            "example":{
                "title":"A new Book",
                "author": "Souvick",
                "description":"Describe the book",
                "rating": 5,
                "published_date": "08/08/2002"
            }
        }
    }

BOOKS=[
    Book(1,"Computer Science Pro", "Souvick","A very nice book!", 5,"08-08-2002"),
    Book(2,"Be fast with FastAPI", "Souvick","Great book!", 5,"08-08-2003"),
    Book(3,"Let us C", "Souvick","An awesome book!", 3,"08-08-2004"),
    Book(4,"HP1", "Author 1","Book Description", 2,"08-08-2005"),
    Book(5,"DD1", "Author 2","Book Description", 4,"08-08-2005"),
    Book(6,"CP4", "Author 3","Book Description", 1,"08-08-2006")
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404, detail="Item Not Found")

@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return=[]
    for book in BOOKS:
        if book.rating==book_rating:
            books_to_return.append(book)
    return books_to_return

@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    # new_book=Book(**book_request.dict()) # ** this will allow the book_request to expand those key value pair into keyword argument that is needed for constructor
    new_book=Book(**book_request.model_dump())
    print(type(new_book))
    # new_book=find_book_id(new_book)
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    book.id=BOOKS[-1].id+1 if len(BOOKS)>0 else 1
    # if len(BOOKS)>0:
    #     book.id=BOOKS[-1].id+1
    # else:
    #     book.id=1
    return book

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changes=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=Book(**book.model_dump())
            book_changes=True
    if not book_changes:
        raise HTTPException(status_code=404,detail="Item not found" )



@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changes=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            book_changes=True
            break
    if not book_changes:
        raise HTTPException(status_code=404,detail="Item not found")
    


@app.get("/books/publish/{pb_date}",status_code=status.HTTP_200_OK)
async def filter_by_published_date(pb_date: str):
    l=[]
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date==pb_date:
            l.append(BOOKS[i])
    return l
    



    