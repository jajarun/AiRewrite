#!/usr/bin/env python3
"""
FastAPI 服务器启动脚本
"""
import uvicorn
from src.server.app import app

if __name__ == "__main__":
    uvicorn.run("src.server.app:app", host="0.0.0.0", port=8000, reload=True) 