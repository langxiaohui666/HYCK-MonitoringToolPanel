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

---

## 📁 项目结构

```text
HYCK-Monitoring-Tool-Panel/
├── api/
├── config/
├── images/
├── main/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   └── wsgi.py
├── models/
├── scripts/
│   ├── init_db.py
│   └── install.sh
├── utils/
├── .env.example
├── LICENSE
└── README.md
🚀 快速开始
方式一：一键安装（推荐）
bash
复制代码
curl -fsSL https://raw.githubusercontent.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/main/scripts/install.sh | bash
安装完成后，终端会提示启动方式。

方式二：手动安装
bash
复制代码
git clone https://github.com/langxiaohui666/HYCK-Monitoring-Tool-Panel.git
cd HYCK-Monitoring-Tool-Panel

python3 -m venv venv
source venv/bin/activate

pip install -r main/requirements.txt

cp .env.example .env

python scripts/init_db.py
python main/app.py
⚡ 访问验证
浏览器访问：

text
复制代码
http://127.0.0.1:5000
如果能访问，说明服务启动成功 ✅

🌐 Nginx 反向代理示例（可选）
nginx
复制代码
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
📸 界面预览
后续可替换为真实截图

<div align="center">

</div>
📄 License
MIT License © langxiaohui666

yaml
复制代码

---

## ✅ 你现在只需要做一件事

```bash
git add README.md
git commit -m "fix: add quick start section and fix anchors"
git push
