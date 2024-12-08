import API
import Database

import uvicorn
# from API.method_api import app
# 引用 FastAPI 实例

if __name__ == '__main__':
    uvicorn.run("API.method_api:app", host="127.0.0.1", port=8000, reload=True)