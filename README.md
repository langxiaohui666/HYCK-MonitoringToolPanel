# <img src="images/logo.png" width="40" height="40" align="right" /> HYCK Monitoring Tool Panel

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)

**一个轻量级、可部署的 Linux 服务器监控工具面板**  
**基于 Python，适合 VPS / 云服务器 / 宝塔面板**

[📚 使用文档](#-快速开始) ·
[📸 界面预览](#-界面预览) ·
[🐛 问题反馈](https://github.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/issues)

</div>

---

## ✨ 项目特性

- CPU / 内存 / 磁盘 / 网络信息采集
- Python 后端，结构清晰，易扩展
- 一键安装脚本，快速部署
- 支持 Nginx 反向代理
- 低资源占用，适合小内存服务器
是一个功能强大的**Linux 服务器监控面板**，旨在帮助用户监控和管理服务器状态。它提供实时监控、性能分析、告警通知和可视化报告等功能，让您更轻松地维护服务器的健康运行。

![HYCK Logo](占位网址https://via.placeholder.com/150x60?text=Logo)  
*(插入此处的LOGO图片链接)*

---

## 功能特点

- **实时监控**：  
  实时捕获 CPU、内存、磁盘使用率和网络流量的详细信息。

- **性能分析**：  
  提供关键性能指标的可视化报告，帮助快速发现系统瓶颈。

- **告警通知**：  
  针对异常情况设定监控阈值，并通过邮件、钉钉或微信推送告警信息。

- **可视化展示**：  
  现代化的科技感 UI 界面，数据可通过动态图表实时展示。

- **易于部署**：  
  开箱即用，支持 systemd、Nginx 反向代理等。

## 快速开始

以下是快速启动 HYCK Monitoring Tool Panel 的步骤：

### 1. 克隆代码

```bash
git clone https://github.com/langxiaohui666/HYCK-MonitoringToolPanel.git
cd HYCK-MonitoringToolPanel
```

### 2. 安装依赖

假设你已经安装了 Python3 和 pip：

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 配置环境变量

复制示例环境变量文件，修改关键参数：

```bash
cp .env.example .env
vim .env  # 编辑配置
```

### 4. 运行项目

#### 开发模式

```bash
python server_monitor.py
```

#### 生产模式 (推荐)

使用 Systemd 和 Gunicorn 运行：

- 配置文件路径：`deploy/server_monitor.service`  

```bash
sudo cp deploy/server_monitor.service /etc/systemd/system/server_monitor.service
sudo systemctl daemon-reload
sudo systemctl start server_monitor
sudo systemctl enable server_monitor
```

使用浏览器访问 `[http://your-server-ip:5000](http://your-server-ip:5000)`，即可查看面板！

---

## Nginx 配置示例

结合 HTTPS 和 Basic Auth 反向代理，推荐配置文件路径：`deploy/nginx_monitor.conf`。

样例如下：

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path_to_ssl/fullchain.pem;
    ssl_certificate_key /path_to_ssl/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }
}
```

---

## 许可协议

本项目使用 [MIT License](https://opensource.org/licenses/MIT) 许可证。

---

## 贡献指南

欢迎所有开发者提交改进建议或功能特性，请通过 GitHub Issues 或 Pull Requests 和我们联系。

当前开放事项：

- 条目1: 添加更多告警通道支持（如 SMS）
- 条目2: 实现 Docker 容器化部署

详见 [Issues 页面](https://github.com/langxiaohui666/HYCK-MonitoringToolPanel/issues)。

---

如有问题，请通过 [langxiaohui666@users.noreply.github.com](mailto:langxiaohui666@users.noreply.github.com) 联系。

