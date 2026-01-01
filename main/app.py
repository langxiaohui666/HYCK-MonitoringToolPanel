#!/usr/bin/env python3
"""
HYCK Monitoring Tool Panel - 主应用文件
"""

import os
import logging
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 加载配置
from config import get_config
app.config.from_object(get_config())

# 启用CORS
CORS(app)

# 初始化扩展
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 用户模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# API路由
@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'HYCK Monitoring Panel',
        'version': '1.0.0'
    })

@app.route('/api/v1/system/info', methods=['GET'])
def system_info():
    """获取系统信息"""
    import platform
    import psutil
    
    info = {
        'system': {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
            'python_version': platform.python_version(),
        },
        'cpu': {
            'cores': psutil.cpu_count(logical=False),
            'logical_cores': psutil.cpu_count(logical=True),
            'usage_percent': psutil.cpu_percent(interval=1),
        },
        'memory': {
            'total': psutil.virtual_memory().total,
            'available': psutil.virtual_memory().available,
            'used': psutil.virtual_memory().used,
            'percent': psutil.virtual_memory().percent,
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'free': psutil.disk_usage('/').free,
            'percent': psutil.disk_usage('/').percent,
        },
        'boot_time': psutil.boot_time(),
        'timestamp': datetime.utcnow().isoformat(),
    }
    
    return jsonify(info)

@app.route('/api/v1/system/processes', methods=['GET'])
def get_processes():
    """获取进程列表"""
    import psutil
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return jsonify({
        'processes': processes,
        'count': len(processes),
        'timestamp': datetime.utcnow().isoformat(),
    })

# 创建数据库表
with app.app_context():
    db.create_all()
    logger.info("数据库表创建完成")
    
    # 创建默认管理员
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@localhost',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        logger.info("默认管理员创建完成")

# 首页
@app.route('/')
def index():
    return jsonify({
        'name': 'HYCK Monitoring Tool Panel',
        'version': '1.0.0',
        'description': '现代化的Linux服务器监控面板',
        'endpoints': {
            'api_health': '/api/health',
            'api_v1': '/api/v1',
            'system_info': '/api/v1/system/info',
            'processes': '/api/v1/system/processes'
        }
    })

if __name__ == '__main__':
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 3000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
