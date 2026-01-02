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

好的！
下面是您的开源服务器监控面板【monitoring-panel】全套项目文件/内容，以 Markdown+分隔横线组织（每一节用文件名标记）。
你只需依次复制对应内容到新建本地文件，保持目录结构，然后 push 到 GitHub 仓库即可一步到位。
— 含 gunicorn systemd、nginx模板、中英双语前端、China+UTC+Local多时区、多语言README。
所有 placeholder（LOGO等）你可后续自定义上传图片和高清视频演示即可。

server_monitor.py
import os
from flask import Flask， jsonify， render_template， request， Response， redirect， url_for
import psutil
from datetime import datetime， timedelta
import pytz

多语言配置
LANGUAGES = {
“zh”： {
“title”： “Linux 服务器实时监控面板”，
“cpu”： “CPU 信息”，
“mem”： “内存 信息”，
“disk”： “磁盘 信息”，
“net”： “网络 信息”，
“load”： “系统 负载 & 状态”，
“core”： “核心数”，
“usage”： “使用率”，
“used”： “已使用”，
“total”： “总”，
“percent”： “使用率”，
“sent”： “累计上传”，
“recv”： “累计下载”，
“sent_rate”： “上行速率”，
“recv_rate”：“下行速率”，
“load1”： “1分钟负载”，
“load5”： “5分钟负载”、“
load15”： “15分钟负载”、“
monitor_time”： “监控时间”、“
status”： “服务状态”，
“uptime”： “运行时间”，
“hostname”： “主机名”，
“os”： “系统”，
“kernel”： “内核”，
“ip”： “公网IP”、“
running”： “正常运行中”，
“history”： “历史 （最近30次样本）”，
“lang_switch”： “切换语言”，
“china_time”：“北京时间”，
“utc_time”：“UTC 时间”，
“local_time”：“本地时间”
}，
“en”： {
“title”： “Linux Server 实时监控面板”，
“CPU”： “CPU 信息”，
“mem”： “内存信息”，
“disk”： “磁盘信息”、“
net”： “网络信息”、“
load”： “系统加载与状态”、“
core”： “核心”，
“使用”： “使用”，
“used”：
“total”， “total”，
“percent”： “使用量”，
“send”： “总计”上传“、”
recv“：”总下载量“、”
sent_rate“：”上行速度“、”
recv_rate“：”下行速度“、”
load1“：”1分钟加载“、”
load5“：”5分钟加载“、”
load15“：”15分钟加载“、”
monitor_time“：”监控时间“、”
status“：”状态
“、”正常运行时间“、
”hostname“：”主机名“、”
os“：”OS“、”
内核“：”内核“、”
ip“：”公共IP“，
“running”：“运行中”，
“history”：“历史（最近30个样本）”，
“lang_switch”：“切换语言”，
“china_time”：“中国时间”，
“utc_time”：“UTC时间”，
“local_time”：“当地时间”
}
}

def get_lang（）：
lang = request.cookies.get（“lang”， “zh”）如果
lang在LANGUAGES中，则返回lang，否则“zh”

def format_bytes（num）：
对于单位 ['B'，'KB'，'MB'，'GB'，'TB']：
如果 num < 1024：返回
f“{num：.1f} {unit}”
num /= 1024
返回 f“{num：.1f} PB”

def get_china_time（）：
return datetime.now（pytz.timezone（“Asia/Shanghai”））.strftime（“%Y-%m-%d %H：%M：%S”）

def get_utc_time（）：
return Datetime.utcnow（）.strftime（“%Y-%m-%d %H：%M：%S”）

def get_local_time（）：
return datetime.now（）.strftime（“%Y-%m-%d %H：%M：%S”）

app = Flask（name）
app.config[“JSON_AS_ASCII”] = False

基本认证
MONITOR_USER = os.getenv（“MONITOR_USER”，“admin”）MONITOR_PASS
= os.getenv（“MONITOR_PASS”，“password”）

def check_auth（u， p）：
return u == MONITOR_USER 和 p == MONITOR_PASS

def authenticate（）：
return Response（'Auth required'， 401， {'WWW-Authenticate'： 'Basic realm=“Login Required”'}）

def requires_auth（f）：
def decorated（*args， **kwargs）：
auth = request.authorization
如果不是 auth 或 not check_auth（auth.username， auth.password）：
return authenticate（）
return f（*args， **kwargs）
装饰。姓名 = F。姓名
返回 已装饰

last_net = {“sent”： 0， “recv”： 0， “time”： datetime.now（）}

@app.route（“/”）@requires_auth

def index（）：
lang = get_lang（）
返回 render_template（“index.html”，lang=lang，lang_map=语言[lang]，LANGUAGES=语言）

@app.route（“/api/monitor”）@requires_auth

def api_monitor（）：
全局 last_net
# CPU
cpu_percent = psutil.cpu_percent（interval=0.3）
cpu_core = psutil.cpu_count（）

# MEM
mem = psutil.virtual_memory()
mem_total = round(mem.total / (1024**3), 2)
mem_used = round(mem.used / (1024**3), 2)
mem_percent = mem.percent

# DISK
disk = psutil.disk_usage("/")
disk_total = round(disk.total / (1024**3), 2)
disk_used = round(disk.used / (1024**3), 2)
disk_percent = disk.percent

# Load
loadv = os.getloadavg() if hasattr(os, "getloadavg") else (0,0,0)
uptime_seconds = int(datetime.now().timestamp() - psutil.boot_time())
uptime_str = str(timedelta(seconds=uptime_seconds))

# Network
net = psutil.net_io_counters()
now = datetime.now()
sent, recv = net.bytes_sent, net.bytes_recv
elapsed = (now - last_net["time"]).total_seconds() or 1
sent_rate = (sent - last_net["sent"]) / elapsed
recv_rate = (recv - last_net["recv"]) / elapsed
last_net = {"sent": sent, "recv": recv, "time": now}
# MB/s
sent_mb, recv_mb = round(sent / 1024/1024, 2), round(recv / 1024 /1024, 2)
sent_rate_mb, recv_rate_mb = round(max(sent_rate,0) / 1024 / 1024, 3), round(max(recv_rate,0)/1024/1024, 3)

# IP
try:
    import requests
    ip = requests.get("https://api.ipify.org",timeout=2).text
    if len(ip) > 30: ip = None
except Exception:
    ip = None

# 3种时间
timeinfo = {
    "china": get_china_time(),
    "utc": get_utc_time(),
    "local": get_local_time()
}

return jsonify({
    "cpu": {"core": cpu_core, "percent": cpu_percent},
    "mem": {"total": mem_total, "used": mem_used, "percent": mem_percent},
    "disk": {"total": disk_total, "used": disk_used, "percent": disk_percent},
    "load": {"1min": loadv[0], "5min": loadv[1], "15min": loadv[2]},
    "uptime": uptime_str,
    "hostname": os.uname().nodename,
    "sys_name": os.uname().sysname,
    "kernel": os.uname().release,
    "net": {
        "sent_mb": sent_mb, "recv_mb": recv_mb,
        "sent_rate_mb_s": sent_rate_mb, "recv_rate_mb_s": recv_rate_mb,
        "ip": ip
    },
    "time": timeinfo
})
@app.route（“/setlang/”）反
对set_lang（lng）：
resp = redirect（url_for（'index'））
如果 LNG 在 LANGUAGES：
resp.set_cookie（“lang”， lng， max_age=6060 24*365）
返回 resp

if name == “main”：
# 安全生产推荐用 Gunicorn 启动
App.run（host=os.getenv（“MONITOR_HOST”， “0.0.0.0”）， port=int（os.getenv（“MONITOR_PORT”， “5000”））requirements.txt

flask
psutil
gunicorn
pytz
requests
templates/index.html

<title>{{lang_map.title}}</title> <风格> body { font-family：“Segoe UI”，单宽，Arial;背景：线性渐变（135度，#0f172a，#1e293b）; 颜色：#e2e8f0;最小高度：100vh;填充：20px;} .container { max-width：1200px; margin：0 auto;} .title { text-align：center;字体大小：2 rem;字体粗大：700;边距底部：16px;} .logo {text-align：center;margin-bottom：18px;} .sys-info {text-align：center;margin-bottom：18px;} .lang-btn {position：absolute;右：30像素;top：24px;} .card-box {display：grid;grid-template-columns：repeat（auto-fit，minmax（320px，1fr））;gap：18px;} .card {background：RGBA（30,41,59,0.55）;边界半径：13px;填充：18px;} .card-title{font-size：1.06rem;margin-bottom：10px;颜色：#38bdf8;border-bottom：1px 实心 #334155;padding-bottom：8px;} .item{margin：6px 0;display：flex;justify-content：space-between;} .progress{宽度：100%;身高：8平分;背景：RGBA（148,163,184,0.17）;边界半径：6px;边距：8px 0;overflow：hidden;} .progress-bar{height：100%;边界半径：6px;背景：线性梯度（90度，#38bdf8，#818cf8）;} .spark{宽度：100%;高度：36px;} .meta {font-size：0.92rem;颜色：#94a3b8;margin-top：3px;} .time-info {margin：10px 0;font-size：0.97em;color：#0ea5e9;} </风格>
LOGO
中文 |英文
{{lang_map.title}}
{{lang_map.hostname}}： — |{{lang_map.os}}： — |{{lang_map.kernel}}： — |{{lang_map.uptime}}： — |{{lang_map.ip}}： —
{{lang_map.china_time}}： |{{lang_map.UTC_time}}： |{{lang_map.local_time}}：
{{lang_map.cpu}}
{{lang_map.core}}—
{{lang_map.percent}}—
{{lang_map.history}}
{{lang_map.mem}}
{{lang_map.total}}—
{{lang_map.used}}—
{{lang_map.percent}}—
{{lang_map.history}}
{{lang_map.disk}}
{{lang_map.total}}—
{{lang_map.used}}—
{{lang_map.percent}}—
{{lang_map.history}}
{{lang_map.net}}
{{lang_map.sent}}—
{{lang_map.recv}}—
{{lang_map.sent_rate}}—
{{lang_map.recv_rate}}—
MB 和 MB/s
{{lang_map.load}}
{{lang_map.load1}}—
{{lang_map.load5}}—
{{lang_map.load15}}—
{{lang_map.监视时间}}——
{{lang_map.status}}： {{lang_map.running}}
<脚本> cont MAX_POINTS = 30; cont history = {cpu：[]， mem：[]， disk：[]， netRate：[]}; function push（arr，v）{arr.push（v）; if（arr.length>MAX_POINTS） arr.shift（）;} function drawSpark（id， arr， color='#38bdf8'）{const c=document.getElementById（id）;如果（！c）返回;cont ctx=c.getContext（'2d'）;const w=c.width=c.clientWidth，h=c.height=c.clientHeight;ctx.clearRect（0,0，w，h）;如果（arr.length===0）return;const maxV=Math.max（...arr）||1;ctx.beginPath（）;for（设i=0;ires.json（））.then（data=>{ document.getElementById（'cpu-core'）.textContent=data.cpu.core; document.getElementById（'cpu-percent'）.textContent=data.cpu.percent+“%”; document.getElementById（'cpu-bar'）.style.width=data.cpu.percent+“%”; push（history.cpu， data.cpu.percent）;drawSpark（“cpu-spark”，history.cpu，“#38bdf8”）; document.getElementById（'mem-total'）.textContent=data.mem.total+“GB”; document.getElementById（'mem-used'）.textContent=data.mem.used+“GB”; document.getElementById（'mem-percent'）.textContent=data.mem.percent+“%”; document.getElementById（'mem-bar'）.style.width=data.mem.percent+“%”; push（history.mem， data.mem.percent）;drawSpark（“mem-spark”，history.mem，“#60a5fa”）; document.getElementById（'disk-total'）.textContent=data.disk.total+“GB”; document.getElementById（'disk-used'）.textContent=data.disk.used+“GB”; document.getElementById（'disk-percent'）.textContent=data.disk.percent+“%”; document.getElementById（'disk-bar'）.style.width=data.disk.percent+“%”; push（history.disk， data.disk.percent）;drawSpark（“disk-spark”，history.disk，“#a78bfa”）; document.getElementById（'net-sent'）.textContent=data.net.sent_mb+“ MB”; document.getElementById（'net-recv'）.textContent=data.net.recv_mb+“ MB”; document.getElementById（'net-sent-rate'）.textContent=data.net.sent_rate_mb_s+“ MB/s”; document.getElementById（'net-recv-rate'）.textContent=data.net.recv_rate_mb_s+“ MB/s”; push（history.netRate，data.net.sent_rate_mb_s+data.net.recv_rate_mb_s）; drawSpark（“net-spark”，history.netRate，“#34d399”）; document.getElementById（'load-1min'）.textContent=data.load['1min']; document.getElementById（'load-5min'）.textContent=data.load['5min']; document.getElementById（'load-15min'）.textContent=data.load['15min']; document.getElementById（'monitor-time'）.textContent=data.time.china; document.getElementById（'uptime'）.textContent=data.uptime; document.getElementById（'hostname'）.textContent=data.hostname; document.getElementById（'sysname'）.textContent=data.sys_name; document.getElementById（'kernel'）.textContent=data.kernel; document.getElementById（'ip'）.textContent=data.net.ip||”—"; document.getElementById（'china-time'）.textContent=data.time.china; document.getElementById（'utc-time'）.textContent=data.time.utc; document.getElementById（'local-time'）.textContent=data.time.local; });} window.onload=function（）{updateData（）;setInterval（updateData，3000）;} </脚本> 部署/server_monitor.service [单位] Description=服务器监控面板（Gunicorn） After=network.target
[服务]
User=monitor
Group=monitor
WorkingDirectory=/opt/monitor
EnvironmentFile=/opt/monitor/.env
ExecStart=/opt/monitor/venv/bin/gunicorn --workers 2 --threads 2 --bind 127.0.0.1：5000 server_monitor：app
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[安装]
WantedBy=multi-user.target
deploy/nginx_monitor.conf
server {
listen 80;
server_name example.com;
return 301 https：//$host$request_uri;
}
服务器 {
听 443 SSLhttp2;
server_name example.com;

ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

auth_basic "Restricted";
auth_basic_user_file /etc/nginx/.htpasswd;

add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options DENY;
add_header Referrer-Policy no-referrer;

location / {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_pass http://127.0.0.1:5000;
    proxy_read_timeout 90;
    proxy_connect_timeout 5s;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
}
client_max_body_size 1m;
}
.env.example
MONITOR_USER=admin
MONITOR_PASS=yourpassword
MONITOR_PORT=5000
MONITOR_HOST=127.0.0.1
.gitignore
*.pyc
pycache/
venv/
*.log
.env
LICENSE
MIT License

版权所有 （c） 2026 鹄鹰长空监测面板

特此免费授权任何获得该副本
的人......
（其余 MIT 协议标准内容）
