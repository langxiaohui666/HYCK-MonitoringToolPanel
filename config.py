"""
HYCK监控面板配置文件
"""

import os
from datetime import timedelta

# 基础配置
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """基础配置类"""
    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(BASE_DIR, "data", "hyck.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 监控配置
    MONITOR_INTERVAL = 5  # 监控间隔（秒）
    HISTORY_DAYS = 7      # 历史数据保留天数
    ALERT_THRESHOLDS = {
        'cpu': 80.0,      # CPU使用率告警阈值（%）
        'memory': 85.0,   # 内存使用率告警阈值（%）
        'disk': 90.0,     # 磁盘使用率告警阈值（%）
        'temperature': 80.0,  # CPU温度告警阈值（℃）
    }
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Docker配置
    DOCKER_ENABLED = os.environ.get('DOCKER_ENABLED', 'false').lower() == 'true'
    DOCKER_SOCKET_PATH = os.environ.get('DOCKER_SOCKET_PATH', '/var/run/docker.sock')
    
    # 管理员配置
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@localhost')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    # API配置
    API_PREFIX = '/api/v1'
    API_RATE_LIMIT = '100 per minute'
    
    # CORS配置
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # 数据保留策略
    DATA_RETENTION = {
        'system_metrics': 30,      # 30天
        'monitor_events': 90,      # 90天
        'audit_logs': 365,         # 365天
    }

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data', 'hyck-dev.db')
    SECRET_KEY = 'dev-secret-key'
    LOG_LEVEL = 'DEBUG'
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ['SECRET_KEY']
    LOG_LEVEL = 'INFO'

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

def get_config(env=None):
    """获取配置类"""
    env = env or os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
