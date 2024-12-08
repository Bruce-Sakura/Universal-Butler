# Basic/API/login.py
from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import RedirectResponse
from Basic.Database.connect import connect_database
from pydantic import BaseModel

router = APIRouter()

# 定义请求体模型
class UserRequest(BaseModel):
    username: str
    password: str

@router.post("/Login")
async def Login(user: UserRequest, db_cursor: tuple = Depends(connect_database)):
    username = user.username
    password = user.password

    if username == "admin" and password == "admin":  # 简单的示例
        return RedirectResponse(url="/dashboard", status_code=303)  # 重定向到控制面板

    elif username != "admin":
        # 执行查询
        query = "SELECT Password FROM Users WHERE username = %s"  # 占位符防止 SQL 注入
        db_cursor.execute(query, (username,))

        result = db_cursor.fetchone()

        if result:
            # 查询到密码，返回给前端
            password = result[0]
            return {"password": password}
        else:
            raise HTTPException(status_code=404, detail="Username not found")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
