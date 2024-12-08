from fastapi import FastAPI, Depends
from gradio.routes import templates
from starlette.templating import Jinja2Templates
from basic.Database.connect import connect_database
from basic.Database.method_database import select_table_library
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import json

app = FastAPI()
# 设置模板路径为 API 文件夹
templates = Jinja2Templates(directory="API/html")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})

@app.get("/database", response_class=HTMLResponse)
def database(request: Request):
    return templates.TemplateResponse("database.html", {"request": request})

@app.get("/database/Library")
def library(db_cursor: tuple = Depends(connect_database)):
    db, cursor = db_cursor
    result = select_table_library(db, cursor)

    if result:
        return JSONResponse(content=json.loads(result))
    else:
        return {"error": "Failed to fetch data from database."}