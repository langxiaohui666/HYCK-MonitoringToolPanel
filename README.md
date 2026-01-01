# <img src="images/logo.png" width="40" height="40" align="right" /> HYCK Monitoring Tool Panel

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Node.js](https://img.shields.io/badge/node.js-16+-orange.svg)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**一个现代化的多功能 Linux 服务器监控工具面板，具有美观的 UI 设计和丰富的监控功能**

[![演示截图](https://img.shields.io/badge/📺-在线演示-ff69b4.svg)](#演示)
[![文档](https://img.shields.io/badge/📚-使用文档-blue.svg)](#文档)
[![问题反馈](https://img.shields.io/badge/🐛-问题反馈-red.svg)](https://github.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/issues)

</div>

---

## ✨ 特性亮点

### 📊 实时监控面板

* 🖥️ **系统概览**：CPU、内存、磁盘、网络实时使用情况
* 📈 **性能图表**：历史数据可视化，趋势分析
* 🔄 **实时更新**：自动刷新，无需手动操作
* 🚨 **警报系统**：阈值设置，智能通知

### 🔧 系统管理

* ⚙️ **进程管理**：查看、结束、优先级调整
* 💾 **磁盘分析**：空间使用可视化，大文件查找
* 🌐 **网络监控**：连接状态，流量统计
* 🔐 **用户管理**：登录用户，会话控制

### 🎨 现代化 UI

* 🌓 **深色 / 浅色主题**：自动适配系统偏好
* 📱 **响应式设计**：完美适配桌面和移动端
* 🎯 **直观仪表盘**：拖拽式组件布局
* 🚀 **流畅动画**：优雅的过渡效果

### 🔒 安全特性

* 🔐 **多用户支持**：基于角色的访问控制
* 🔑 **OAuth 集成**：支持 GitHub、Google 登录
* 📝 **操作日志**：完整的审计追踪
* 🔒 **HTTPS 支持**：安全的通信传输

---

## 🚀 快速开始

### 系统要求

* **操作系统**：Linux（Ubuntu 20.04+ / CentOS 8+ / Debian 11+）
* **Python**：3.8 或更高版本
* **Node.js**：16.x 或更高版本
* **内存**：最低 512MB RAM
* **磁盘空间**：最低 1GB 可用空间

---

## 📦 一键脚本安装（推荐）

### 1️⃣ 使用自动安装脚本

```bash
# 使用 curl
curl -fsSL https://raw.githubusercontent.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/main/install.sh | bash

# 或使用 wget
wget -qO- https://raw.githubusercontent.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/main/install.sh | bash
```

### 2️⃣ 脚本安装选项

```bash
# 自定义安装目录
curl -fsSL https://raw.githubusercontent.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/main/install.sh | bash -s -- --path /opt/hyck

# 指定端口
curl -fsSL https://raw.githubusercontent.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/main/install.sh | bash -s -- --port 8080

# 完整选项
curl -fsSL https://raw.githubusercontent.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/main/install.sh | bash -s -- \
  --path /opt/hyck \
  --port 8080 \
  --admin-email admin@example.com \
  --with-docker \
  --with-nginx
```

### 3️⃣ 安装后操作

```bash
# 查看服务状态
sudo systemctl status hyck-monitor

# 查看日志
sudo journalctl -u hyck-monitor -f
```

* 默认访问地址：`http://your-server-ip:3000`
* 默认账号：`admin`
* 默认密码：`admin123`

---

## 🐳 Docker Compose 安装（生产环境）

### 1️⃣ 下载配置

```bash
mkdir -p ~/hyck-monitor && cd ~/hyck-monitor

wget https://raw.githubusercontent.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/main/docker-compose.prod.yml
wget https://raw.githubusercontent.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/main/.env.example -O .env
```

### 2️⃣ 配置环境变量

```bash
nano .env
```

```env
HYCK_SECRET_KEY=your-secure-secret-key
HYCK_DB_PASSWORD=your-db-password
HYCK_ADMIN_EMAIL=admin@yourdomain.com
HYCK_DOMAIN=monitor.yourdomain.com
```

### 3️⃣ 启动服务

```bash
docker-compose -f docker-compose.prod.yml up -d

docker-compose -f docker-compose.prod.yml ps

docker-compose -f docker-compose.prod.yml logs -f
```

---

## 🔧 手动分步安装（开发环境）

### 1️⃣ 系统准备

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y \
  python3 python3-pip python3-venv \
  nodejs npm git curl wget \
  build-essential libssl-dev libffi-dev

# CentOS / RHEL
sudo yum install -y epel-release
sudo yum install -y python3 python3-pip \
  nodejs npm git curl wget \
  gcc make openssl-devel
```

### 2️⃣ 下载源码

```bash
git clone https://github.com/langxiaohui666/HYCK-Monitoring-Tool-Panel.git
cd HYCK-Monitoring-Tool-Panel

git checkout v1.0.0
```

### 3️⃣ 后端安装

```bash
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements/production.txt

python scripts/init_database.py

cp config/config.example.yaml config/config.yaml
cp .env.example .env
```

### 4️⃣ 前端安装

```bash
cd frontend
npm install --production
npm run build
cd ..
```

### 5️⃣ systemd 服务配置

```bash
sudo cp systemd/hyck-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hyck-monitor
sudo systemctl start hyck-monitor
```

### 6️⃣ Nginx 反向代理（可选）

```nginx
server {
    listen 80;
    server_name monitor.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🌐 宝塔面板安装（简单快捷）

### 1️⃣ 安装依赖

* Nginx 1.20+
* Python 3.8+
* PM2 管理器
* MySQL 或 PostgreSQL

### 2️⃣ 部署步骤

```bash
cd /www/wwwroot
git clone https://github.com/langxiaohui666/HYCK-Monitoring-Tool-Panel.git
cd HYCK-Monitoring-Tool-Panel

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd frontend
npm install
npm run build
cd ..

python app.py &
```

### 3️⃣ 宝塔网站配置

* 站点域名：`monitor.yourdomain.com`
* 根目录：`/www/wwwroot/HYCK-Monitoring-Tool-Panel/frontend/dist`
* 反向代理：`http://127.0.0.1:5000`
* 开启 SSL 证书

---

## ⚡ 快速验证安装

```bash
curl http://localhost:3000/api/health
curl http://localhost:3000/api/version
curl http://localhost:3000/api/v1/system/info
```

---

## 📸 界面预览

<div align="center">

**🎯 主仪表盘**
[https://via.placeholder.com/800x450/1e293b/ffffff?text=Dashboard+Preview](https://via.placeholder.com/800x450/1e293b/ffffff?text=Dashboard+Preview)

**📊 系统监控**
[https://via.placeholder.com/800x450/1e293b/ffffff?text=System+Monitoring](https://via.placeholder.com/800x450/1e293b/ffffff?text=System+Monitoring)

**🔧 进程管理**
[https://via.placeholder.com/800x450/1e293b/ffffff?text=Process+Management](https://via.placeholder.com/800x450/1e293b/ffffff?text=Process+Management)

</div>

---

## 📄 License

This project is licensed under the **MIT License**.
