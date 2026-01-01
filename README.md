# <img src="images/logo.png" width="40" height="40" align="right" /> HYCK Monitoring Tool Panel

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Node.js](https://img.shields.io/badge/python-backend-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**一个现代化、轻量级、可部署的 Linux 服务器监控工具面板**
**基于 Python，适合 VPS / 宝塔 / 云服务器 使用**

[📺 在线演示](#界面预览) · [📚 使用文档](#快速开始) · [🐛 问题反馈](https://github.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/issues)

</div>

---

## ✨ 项目特性

### 📊 系统监控

* CPU / 内存 / 磁盘 / 网络实时监控
* 系统运行状态概览
* 轻量级、低资源占用

### 🔧 服务能力

* 后端 API 架构清晰
* 支持环境变量配置
* 数据库初始化脚本

### 🎨 UI 设计

* 简洁现代风格
* 适配桌面 / 服务器管理场景
* 易于二次开发

### 🔒 安全性

* 环境变量隔离敏感信息
* 可部署于内网或公网
* 适配 Nginx 反向代理

---

## 📁 项目结构

```text
HYCK-Monitoring-Tool-Panel/
├── api/                # API 接口
├── config/             # 配置文件
├── images/             # README 资源
├── main/               # 主程序
│   ├── app.py          # 应用入口
│   ├── config.py       # 主配置
│   ├── requirements.txt
│   └── wsgi.py
├── models/             # 数据模型
├── scripts/            # 脚本工具
│   ├── init_db.py      # 数据库初始化
│   └── install.sh      # 一键安装脚本
├── utils/              # 工具函数
├── .env.example        # 环境变量示例
└── README.md
```

---

## 🚀 快速开始

### 方式一：一键安装（推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/main/scripts/install.sh | bash
```

---

### 方式二：手动安装（开发 / 调试）

#### 1️⃣ 克隆项目

```bash
git clone https://github.com/langxiaohui666/HYCK-Monitoring-Tool-Panel.git
cd HYCK-Monitoring-Tool-Panel
```

#### 2️⃣ 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ 安装依赖

```bash
pip install -r main/requirements.txt
```

#### 4️⃣ 配置环境变量

```bash
cp .env.example .env
nano .env
```

#### 5️⃣ 初始化数据库

```bash
python scripts/init_db.py
```

#### 6️⃣ 启动服务

```bash
python main/app.py
```

---

## ⚡ 服务验证

```bash
# 健康检查
curl http://127.0.0.1:5000/
```

---

## 🌐 Nginx 反向代理示例（可选）

```nginx
server {
    listen 80;
    server_name monitor.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📸 界面预览

<div align="center">

![Dashboard](https://via.placeholder.com/800x450/1e293b/ffffff?text=HYCK+Monitoring+Dashboard)

</div>

---

## 🧩 开发计划（Roadmap）

* [ ] 前端可视化仪表盘
* [ ] 告警通知（邮件 / Webhook）
* [ ] Docker 部署支持
* [ ] 多节点监控

---

## 📄 License

This project is licensed under the **MIT License**.

---

> 💡 项目作者：浪晓回（langxiaohui666）
> ⭐ 如果这个项目对你有帮助，欢迎 Star 支持
