#!/bin/bash

# PDF认证工具系统服务卸载脚本
# PDF Certification Tool System Service Uninstall Script

set -e

echo "正在卸载PDF认证工具系统服务..."
echo "Uninstalling PDF Certification Tool system service..."

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "错误: 请使用sudo运行此脚本"
    echo "Error: Please run this script with sudo"
    exit 1
fi

# 停止服务
echo "停止服务..."
echo "Stopping service..."
systemctl stop pdf-certification.service 2>/dev/null || true

# 禁用服务
echo "禁用服务..."
echo "Disabling service..."
systemctl disable pdf-certification.service 2>/dev/null || true

# 删除服务文件
echo "删除服务文件..."
echo "Removing service file..."
rm -f /etc/systemd/system/pdf-certification.service

# 重新加载systemd配置
echo "重新加载systemd配置..."
echo "Reloading systemd configuration..."
systemctl daemon-reload

# 重置失败的单元
echo "重置失败的单元..."
echo "Resetting failed units..."
systemctl reset-failed 2>/dev/null || true

echo ""
echo "卸载完成！"
echo "Uninstall complete!"
echo ""
echo "注意: 日志文件和上传的文件仍然保留在项目目录中"
echo "Note: Log files and uploaded files are still preserved in the project directory" 