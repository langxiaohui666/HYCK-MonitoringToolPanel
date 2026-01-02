markdown
# Haiying Monitoring Panel / 海鹰服务器监控面板

![logo](占为网址https://img.example.com/logo.png)

---

## 简介 (中文)

一款基于 Python3 + Flask 的开箱即用服务器观测仪表盘，支持多时区切换，中英双语实时切换，含 systemd/Nginx 配置模板，适合自用与生产环境一键部署。
 Project Introduction (English)

A plug-and-play Linux server monitoring dashboard powered by Flask & Python3. It supports realtime data, timezone switch, bilingual (Chinese/English), and contains production systemd/nginx deploy samples.
---
 快速部署/Quick Start
```bash
# 必须已安装 python3/pip
git clone https://github.com/你的用户名/haiyingmonitoring-panel.git
cd haiyingmonitoring-panel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
vim .env   # 设置你的用户名和密码，默认为 admin/yourpassword
# 启动开发
python server_monitor.py
# 推荐生产 systemd + gunicorn
```
### 生产环境 (systemd/推荐)

- 见 deploy/server_monitor.service

```bash
sudo cp deploy/server_monitor.service /etc/systemd/system/server_monitor.service
sudo systemctl daemon-reload
sudo systemctl enable --now server_monitor
# 查看日志
sudo journalctl -u server_monitor -f
```
### Nginx反代+认证
- 见 deploy/nginx_monitor.conf 模板 (注意ssl证书需自配，htpasswd建议用 apache2-utils 生成)
---
## 功能说明 / Features
- 实时显示：CPU / 内存 / 磁盘 / 网络速率/ 公网IP
- 美观炫酷前端, 玻璃拟态风, 折线历史小图
- 中英双语实时切换，支持中国/本地/UTC时间显示
- systemd模板, Nginx反代+ HTTPS/Basicauth
- All features support English/Chinese, multi-timezone, production deployment
---
## 截图 / Screenshots
![仪表盘总览](占位网址https://img.example.com/screenshot1.png)
---
## LOGO/演示/多语言拓展
- LOGO/截图可在 templates/index.html & 本文手动替换
- 如需嵌入演示视频，请上传 mp4/gif 到你的cdn/图床或YouTube/BiliBili，填入链接即可
- 所有前端字符串支持扩展其它语言（参见 LANGUAGES 结构/多语言模块）

---

## License

MIT License.
