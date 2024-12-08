# Basic/API/method_api.py
from fastapi import APIRouter, Depends
from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import json

from Basic.Database.connect import connect_database
from Basic.Database.method_database import select_table_library, select_table_Items

router = APIRouter()

# 设置模板路径为 API 文件夹
templates = Jinja2Templates(directory="Basic/API/html")

@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})

@router.get("/database", response_class=HTMLResponse)
def database(request: Request):
    return templates.TemplateResponse("database.html", {"request": request})

@router.get("/database/Library")
def library(db_cursor: tuple = Depends(connect_database)):
    db, cursor = db_cursor
    result = select_table_library(db, cursor)

    if result:
        return JSONResponse(content=json.loads(result))
    else:
        return {"error": "Failed to fetch data from database."}

@router.get("/database/Items")
def Items(db_cursor: tuple = Depends(connect_database)):
    db, cursor = db_cursor
    result = select_table_Items(db, cursor)

    if result:
        return JSONResponse(content=json.loads(result))
    else:
        return {"error": "Failed to fetch data from database."}
