from fastapi import APIRouter, HTTPException, Depends
from Basic.Database.connect import connect_database
from pydantic import BaseModel
import logging

router = APIRouter()

# 定义请求体模型
class UserRequest(BaseModel):
    username: str
    password: str

@router.post("/Login")
async def Login(user: UserRequest, db_cursor: tuple = Depends(connect_database)):
    db, cursor = db_cursor  # 解包数据库连接和游标
    if db is None or cursor is None:  # 如果连接失败，返回500错误
        raise HTTPException(status_code=500, detail="Database connection failed")

    username = user.username
    password = user.password

    try:
        # 执行查询，查询用户名是否存在
        query = "SELECT Password FROM Users WHERE username = %s"  # 占位符防止 SQL 注入
        cursor.execute(query, (username,))

        result = cursor.fetchone()

        if result:
            # 查询到密码，验证密码是否正确
            stored_password = result['Password']  # 使用字典方式访问字段
            if stored_password == password:  # 密码匹配
                logging.info(f"User {username} logged in successfully")
                return {"message": "Login successful", "status": "success"}  # 返回成功
            else:  # 密码不匹配
                logging.warning(f"Invalid login attempt for user {username}: Incorrect password")
                raise HTTPException(status_code=401, detail="Invalid credentials")
        else:
            # 用户名未找到
            logging.warning(f"Invalid login attempt: Username {username} not found")
            raise HTTPException(status_code=404, detail="Username not found")

    except Exception as e:
        # 捕获任何异常，记录日志并返回 500 错误
        logging.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        # 确保连接在操作完成后关闭
        cursor.close()
        db.close()
        print("Database (login) connection closed...")
