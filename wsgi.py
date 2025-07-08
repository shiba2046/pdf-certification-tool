#!/usr/bin/env python3
"""
WSGI entry point for PDF certification tool
生产环境WSGI入口点
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from flask import request

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置环境变量
os.environ.setdefault('FLASK_ENV', 'production')

# 配置日志
if not os.path.exists('logs'):
    os.makedirs('logs')

# 配置日志格式
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

# 文件日志处理器
file_handler = RotatingFileHandler(
    'logs/pdf_certification.log', 
    maxBytes=10240000,  # 10MB
    backupCount=10
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# 控制台日志处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# 配置Flask应用日志
from app import app
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

# IP地址日志中间件
@app.before_request
def log_ip_address():
    # 获取客户端IP地址
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        # 如果使用代理，获取真实IP
        client_ip = x_forwarded_for.split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        # Nginx代理的真实IP
        client_ip = request.headers.get('X-Real-IP')
    else:
        # 直接连接的IP
        client_ip = request.remote_addr
    
    # 记录访问日志
    app.logger.info(f"IP访问: {client_ip} - {request.method} {request.path} - User-Agent: {request.headers.get('User-Agent', 'Unknown')}")

# 确保必要的目录存在
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)

# Load environment variables from .env file
load_dotenv()
if __name__ == "__main__":
    app.run(host="0.0.0.0") 