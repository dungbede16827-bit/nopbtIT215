from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Programming",
        "author": "Nguyen Van A",
        "category": "programming",
        "year": 2020,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Learning FastAPI",
        "author": "Tran Thi B",
        "category": "web",
        "year": 2023,
        "is_available": True
    },
    {
        "id": 3,
        "title": "Database Design",
        "author": "Le Van C",
        "category": "database",
        "year": 2021,
        "is_available": False
    },
    {
        "id": 4,
        "title": "Computer Networks",
        "author": "Pham Van D",
        "category": "network",
        "year": 2019,
        "is_available": True
    },
    {
        "id": 5,
        "title": "Advanced Python",
        "author": "Hoang Thi E",
        "category": "programming",
        "year": 2022,
        "is_available": False
    },
    {
        "id": 6,
        "title": "FastAPI Basic",
        "author": "Nguyen Van A",
        "category": "web",
        "year": 2024,
        "is_available": True
    }
]

@app.get("/books/available")
def get_available_books():
    result = []

    for book in books:
        if book["is_available"] == True:
            result.append(book)

    return result


@app.get("/books/borrowed")
def get_borrowed_books():
    result = []

    for book in books:
        if book["is_available"] == False:
            result.append(book)

    return result

