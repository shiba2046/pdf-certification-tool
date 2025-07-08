#!/bin/bash
# PDF认证工具启动脚本
# 启动脚本用于systemd服务

cd /home/ubuntu/apps/pdf-certification-tool

# 激活虚拟环境
source .venv/bin/activate

# 启动gunicorn
exec gunicorn --workers 4 --bind 0.0.0.0:5000 --access-logfile logs/access.log --error-logfile logs/error.log wsgi:app 