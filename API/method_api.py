from fastapi import FastAPI, Depends
from Database.method_database import connect_database
from Database.method_database import select_table_library
from starlette.responses import JSONResponse
import json
app = FastAPI()

@app.get("/")
def root():
    return """
            Hello, World!\n
            This is an API.\n
            Nice to meet you!\n
            \n
            API Endpoints Structure:\n
            ├── /\n
            │   ├── /database\n
            │       ├── /database/Library\n
            """

@app.get("/database")
def database():
    return {"message": "Hello, Database!\n This is a Database.\n Nice to meet you!"}

@app.get("/database/Library")
def library(db_cursor: tuple = Depends(connect_database)):
    db, cursor = db_cursor
    result = select_table_library(db, cursor)

    if result:
        return JSONResponse(content=json.loads(result))
    else:
        return {"error": "Failed to fetch data from database."}

