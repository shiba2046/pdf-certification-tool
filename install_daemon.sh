#!/bin/bash

# PDF认证工具系统服务安装脚本
# PDF Certification Tool System Service Installation Script

set -e

echo "正在安装PDF认证工具系统服务..."
echo "Installing PDF Certification Tool system service..."

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "错误: 请使用sudo运行此脚本"
    echo "Error: Please run this script with sudo"
    exit 1
fi

# 获取当前用户和组
CURRENT_USER=$(logname || echo $SUDO_USER)
CURRENT_GROUP=$(id -gn $CURRENT_USER)

echo "检测到用户: $CURRENT_USER, 组: $CURRENT_GROUP"
echo "Detected user: $CURRENT_USER, group: $CURRENT_GROUP"

# 获取项目根目录
PROJECT_DIR=$(pwd)
echo "项目目录: $PROJECT_DIR"
echo "Project directory: $PROJECT_DIR"

# 更新服务文件中的用户和路径
sed -i "s/User=ubuntu/User=$CURRENT_USER/g" pdf-certification.service
sed -i "s/Group=ubuntu/Group=$CURRENT_USER/g" pdf-certification.service
sed -i "s|WorkingDirectory=/home/ubuntu/apps/pdf-certification-tool|WorkingDirectory=$PROJECT_DIR|g" pdf-certification.service
sed -i "s|Environment=PATH=/home/ubuntu/apps/pdf-certification-tool/.venv/bin|Environment=PATH=$PROJECT_DIR/.venv/bin|g" pdf-certification.service
sed -i "s|ExecStart=/home/ubuntu/apps/pdf-certification-tool/.venv/bin/gunicorn|ExecStart=$PROJECT_DIR/.venv/bin/gunicorn|g" pdf-certification.service
sed -i "s|ReadWritePaths=/home/ubuntu/apps/pdf-certification-tool/logs /home/ubuntu/apps/pdf-certification-tool/uploads /home/ubuntu/apps/pdf-certification-tool/processed|ReadWritePaths=$PROJECT_DIR/logs $PROJECT_DIR/uploads $PROJECT_DIR/processed|g" pdf-certification.service

# 安装gunicorn依赖
echo "安装gunicorn依赖..."
echo "Installing gunicorn dependency..."
if command -v uv &> /dev/null; then
    uv add --active gunicorn
else
    echo "警告: 未找到uv，请手动安装gunicorn"
    echo "Warning: uv not found, please install gunicorn manually"
fi

# 创建必要的目录
echo "创建必要的目录..."
echo "Creating necessary directories..."
mkdir -p logs
mkdir -p uploads
mkdir -p processed

# 设置目录权限
echo "设置目录权限..."
echo "Setting directory permissions..."
chown -R $CURRENT_USER:$CURRENT_GROUP logs uploads processed
chmod 755 logs uploads processed

# 复制服务文件到systemd目录
echo "安装systemd服务..."
echo "Installing systemd service..."
cp pdf-certification.service /etc/systemd/system/

# 重新加载systemd配置
echo "重新加载systemd配置..."
echo "Reloading systemd configuration..."
systemctl daemon-reload

# 启用服务
echo "启用服务..."
echo "Enabling service..."
systemctl enable pdf-certification.service

# 启动服务
echo "启动服务..."
echo "Starting service..."
systemctl start pdf-certification.service

# 检查服务状态
echo "检查服务状态..."
echo "Checking service status..."
systemctl status pdf-certification.service --no-pager

echo ""
echo "安装完成！"
echo "Installation complete!"
echo ""
echo "服务管理命令:"
echo "Service management commands:"
echo "  启动服务: sudo systemctl start pdf-certification"
echo "  Start service: sudo systemctl start pdf-certification"
echo "  停止服务: sudo systemctl stop pdf-certification"
echo "  Stop service: sudo systemctl stop pdf-certification"
echo "  重启服务: sudo systemctl restart pdf-certification"
echo "  Restart service: sudo systemctl restart pdf-certification"
echo "  查看状态: sudo systemctl status pdf-certification"
echo "  Check status: sudo systemctl status pdf-certification"
echo "  查看日志: sudo journalctl -u pdf-certification -f"
echo "  View logs: sudo journalctl -u pdf-certification -f"
echo ""
echo "应用将在 http://localhost:5000 上运行"
echo "Application will be running at http://localhost:5000" 