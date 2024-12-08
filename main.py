# main.py
import uvicorn
from fastapi import FastAPI
from Basic.API.login import router as login_router
from Basic.API.method_api import router as method_api_router

app = FastAPI(debug=True)  # 开启调试模式

# 将路由注册到 FastAPI 应用中
app.include_router(login_router)   # 包含登录相关路由
app.include_router(method_api_router)  # 包含数据库相关路由

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)  # 修改为导入路径字符串