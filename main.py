# main.py
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from Basic.API.login import router as login_router
from Basic.API.method_api import router as method_api_router

app = FastAPI(debug=True)  # 开启调试模式

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

# 将路由注册到 FastAPI 应用中
app.include_router(login_router)   # 包含登录相关路由
app.include_router(method_api_router)  # 包含数据库相关路由

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)  # 修改为导入路径字符串