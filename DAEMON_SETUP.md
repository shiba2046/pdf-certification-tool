# PDF认证工具系统服务设置指南
# PDF Certification Tool System Service Setup Guide

## 概述 / Overview

本文档介绍如何将PDF认证工具设置为系统守护进程，以便在后台自动运行。
This document describes how to set up the PDF certification tool as a system daemon for automatic background operation.

## 前提条件 / Prerequisites

- Linux系统（支持systemd）
- Python 3.13+
- uv包管理器
- sudo权限

## 安装步骤 / Installation Steps

### 1. 安装依赖 / Install Dependencies

```bash
# 安装gunicorn（如果尚未安装）
uv add --active gunicorn
```

### 2. 运行安装脚本 / Run Installation Script

```bash
sudo ./install_daemon.sh
```

安装脚本将：
The installation script will:

- 自动检测当前用户和项目路径
- Automatically detect current user and project path
- 创建必要的目录（logs, uploads, processed）
- Create necessary directories (logs, uploads, processed)
- 安装systemd服务文件
- Install systemd service file
- 启用并启动服务
- Enable and start the service

### 3. 验证安装 / Verify Installation

```bash
# 检查服务状态
sudo systemctl status pdf-certification

# 查看日志
sudo journalctl -u pdf-certification -f
```

## 服务管理 / Service Management

### 启动服务 / Start Service
```bash
sudo systemctl start pdf-certification
```

### 停止服务 / Stop Service
```bash
sudo systemctl stop pdf-certification
```

### 重启服务 / Restart Service
```bash
sudo systemctl restart pdf-certification
```

### 查看状态 / Check Status
```bash
sudo systemctl status pdf-certification
```

### 查看日志 / View Logs
```bash
# 实时查看日志
sudo journalctl -u pdf-certification -f

# 查看最近的日志
sudo journalctl -u pdf-certification -n 50

# 查看特定时间的日志
sudo journalctl -u pdf-certification --since "2024-01-01 00:00:00"
```

## 配置 / Configuration

### 环境变量 / Environment Variables

服务使用以下环境变量：
The service uses the following environment variables:

- `FLASK_ENV=production` - 生产环境模式
- `FLASK_APP=wsgi.py` - WSGI应用入口点

### 端口配置 / Port Configuration

默认端口：5000
Default port: 5000

如需更改端口，编辑服务文件：
To change the port, edit the service file:

```bash
sudo nano /etc/systemd/system/pdf-certification.service
```

修改ExecStart行中的端口号：
Modify the port number in the ExecStart line:

```
ExecStart=/path/to/gunicorn --workers 4 --bind 0.0.0.0:8080 ...
```

然后重启服务：
Then restart the service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart pdf-certification
```

## 日志文件 / Log Files

应用日志存储在以下位置：
Application logs are stored in the following locations:

- 系统日志：`journalctl -u pdf-certification`
- System logs: `journalctl -u pdf-certification`
- 应用日志：`logs/pdf_certification.log`
- Application logs: `logs/pdf_certification.log`
- 访问日志：`logs/access.log`
- Access logs: `logs/access.log`
- 错误日志：`logs/error.log`
- Error logs: `logs/error.log`

## 卸载 / Uninstallation

运行卸载脚本：
Run the uninstall script:

```bash
sudo ./uninstall_daemon.sh
```

## 故障排除 / Troubleshooting

### 服务无法启动 / Service Won't Start

1. 检查日志：
   Check logs:
   ```bash
   sudo journalctl -u pdf-certification -n 50
   ```

2. 检查权限：
   Check permissions:
   ```bash
   ls -la /home/ubuntu/apps/pdf-certification-tool/
   ```

3. 检查Python环境：
   Check Python environment:
   ```bash
   /home/ubuntu/apps/pdf-certification-tool/.venv/bin/python --version
   ```

### 端口被占用 / Port Already in Use

检查端口使用情况：
Check port usage:

```bash
sudo netstat -tlnp | grep :5000
```

### 权限问题 / Permission Issues

确保目录权限正确：
Ensure correct directory permissions:

```bash
sudo chown -R ubuntu:ubuntu /home/ubuntu/apps/pdf-certification-tool/
sudo chmod 755 /home/ubuntu/apps/pdf-certification-tool/logs
sudo chmod 755 /home/ubuntu/apps/pdf-certification-tool/uploads
sudo chmod 755 /home/ubuntu/apps/pdf-certification-tool/processed
```

## 安全注意事项 / Security Considerations

- 服务以非root用户运行
- Service runs as non-root user
- 使用systemd的安全限制
- Uses systemd security restrictions
- 日志轮转防止磁盘空间耗尽
- Log rotation prevents disk space exhaustion
- 生产环境建议使用反向代理（如nginx）
- Production environments should use reverse proxy (e.g., nginx) 