# PDF认证工具 / PDF Certification Tool

一个用于在PDF文档上添加认证签名的Flask Web应用。
A Flask web application for adding certification signatures to PDF documents.

## 功能特性 / Features

- 上传PDF文件
- Upload PDF files
- 在PDF上添加可自定义的签名框
- Add customizable signature boxes to PDFs
- 支持多种位置和颜色选项
- Support for multiple positions and color options
- 实时预览和下载处理后的文件
- Real-time preview and download of processed files

## 快速开始 / Quick Start

### 开发环境 / Development

```bash
# 安装依赖
uv sync

# 运行开发服务器
python app.py
```

### 生产环境 / Production

将应用设置为系统守护进程：
Set up the application as a system daemon:

```bash
# 安装系统服务
sudo ./install_daemon.sh

# 检查服务状态
sudo systemctl status pdf-certification
```

详细设置说明请参考 [DAEMON_SETUP.md](DAEMON_SETUP.md)
For detailed setup instructions, see [DAEMON_SETUP.md](DAEMON_SETUP.md)

## 使用说明 / Usage

1. 访问 http://localhost:5000
2. 上传PDF文件
3. 选择签名框位置和颜色
4. 添加自定义文本
5. 下载处理后的PDF

## 技术栈 / Tech Stack

- Python 3.13+
- Flask 3.1+
- PyPDF2
- ReportLab
- Gunicorn (生产环境)
- Systemd (系统服务)

## 项目结构 / Project Structure

```
pdf-certification-tool/
├── app.py              # 主应用文件
├── wsgi.py             # WSGI入口点
├── templates/          # HTML模板
├── uploads/           # 上传文件目录
├── processed/         # 处理后文件目录
├── logs/              # 日志文件目录
├── install_daemon.sh  # 安装脚本
├── uninstall_daemon.sh # 卸载脚本
└── DAEMON_SETUP.md    # 守护进程设置文档
```

## 服务管理 / Service Management

```bash
# 启动服务
sudo systemctl start pdf-certification

# 停止服务
sudo systemctl stop pdf-certification

# 重启服务
sudo systemctl restart pdf-certification

# 查看状态
sudo systemctl status pdf-certification

# 查看日志
sudo journalctl -u pdf-certification -f
```

## 卸载 / Uninstallation

```bash
sudo ./uninstall_daemon.sh
```