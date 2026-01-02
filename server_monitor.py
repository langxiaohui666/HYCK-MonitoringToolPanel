import os
from flask import Flask, jsonify, render_template, request, Response, redirect, url_for
import psutil
from datetime import datetime, timedelta
import pytz

# 多语言配置
LANGUAGES = {
    "zh": {
        "title": "Linux 服务器实时监控面板",
        "cpu": "CPU 信息",
        "mem": "内存 信息",
        "disk": "磁盘 信息",
        "net": "网络 信息",
        "load": "系统 负载 & 状态",
        "core": "核心数",
        "usage": "使用率",
        "used": "已使用",
        "total": "总",
        "percent": "使用率",
        "sent": "累计上传",
        "recv": "累计下载",
        "sent_rate": "上行速率",
        "recv_rate": "下行速率",
        "load1": "1分钟负载",
        "load5": "5分钟负载",
        "load15": "15分钟负载",
        "monitor_time": "监控时间",
        "status": "服务状态",
        "uptime": "运行时间",
        "hostname": "主机名",
        "os": "系统",
        "kernel": "内核",
        "ip": "公网IP",
        "running": "正常运行中",
        "history": "历史 (最近30次样本)",
        "lang_switch": "切换语言",
        "china_time":"北京时间",
        "utc_time":"UTC 时间",
        "local_time":"本地时间"
    },
    "en": {
        "title": "Linux Server Realtime Monitoring Panel",
        "cpu": "CPU Info",
        "mem": "Memory Info",
        "disk": "Disk Info",
        "net": "Network Info",
        "load": "System Load & Status",
        "core": "Cores",
        "usage": "Usage",
        "used": "Used",
        "total": "Total",
        "percent": "Usage",
        "sent": "Total Upload",
        "recv": "Total Download",
        "sent_rate": "Up Speed",
        "recv_rate": "Down Speed",
        "load1": "1min Load",
        "load5": "5min Load",
        "load15": "15min Load",
        "monitor_time": "Monitor Time",
        "status": "Status",
        "uptime": "Uptime",
        "hostname": "Hostname",
        "os": "OS",
        "kernel": "Kernel",
        "ip": "Public IP",
        "running": "Running",
        "history": "History (Last 30 samples)",
        "lang_switch": "Switch language",
        "china_time":"China Time",
        "utc_time":"UTC Time",
        "local_time":"Local Time"
    }
}

def get_lang():
    lang = request.cookies.get("lang", "zh")
    return lang if lang in LANGUAGES else "zh"

def format_bytes(num):
    for unit in ['B','KB','MB','GB','TB']:
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} PB"

def get_china_time():
    return datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")

def get_utc_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def get_local_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# Basic Auth
MONITOR_USER = os.getenv("MONITOR_USER", "admin")
MONITOR_PASS = os.getenv("MONITOR_PASS", "password")

def check_auth(u, p):
    return u == MONITOR_USER and p == MONITOR_PASS

def authenticate():
    return Response('Auth required', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

last_net = {"sent": 0, "recv": 0, "time": datetime.now()}

@app.route("/")
@requires_auth
def index():
    lang = get_lang()
    return render_template("index.html", lang=lang, lang_map=LANGUAGES[lang], LANGUAGES=LANGUAGES)

@app.route("/api/monitor")
@requires_auth
def api_monitor():
    global last_net
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.3)
    cpu_core = psutil.cpu_count()

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

@app.route("/setlang/<lng>")
def set_lang(lng):
    resp = redirect(url_for('index'))
    if lng in LANGUAGES:
        resp.set_cookie("lang", lng, max_age=60*60*24*365)
    return resp

if __name__ == "__main__":
    # 安全生产推荐用 gunicorn 启动
    app.run(host=os.getenv("MONITOR_HOST", "0.0.0.0"), port=int(os.getenv("MONITOR_PORT", "5000")))
```