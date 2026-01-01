"""
HYCK监控面板配置文件
"""

import os
from datetime import timedelta

# 基础配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    """基础配置类"""
    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(BASE_DIR, "..", "data", "hyck.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 监控配置
    MONITOR_INTERVAL = 5  # 监控间隔（秒）
    HISTORY_DAYS = 7      # 历史数据保留天数
    ALERT_THRESHOLDS = {
        'cpu': 80.0,      # CPU使用率告警阈值（%）
        'memory': 85.0,   # 内存使用率告警阈值（%）
        'disk': 90.0,     # 磁盘使用率告警阈值（%）
    }
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = os.path.join(BASE_DIR, '..', 'logs', 'app.log')
    
    # Docker配置
    DOCKER_ENABLED = os.environ.get('DOCKER_ENABLED', 'false').lower() == 'true'
    
    # API配置
    API_PREFIX = '/api/v1'

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'dev-secret-key-for-development'
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'production-secret-key')
    LOG_LEVEL = 'WARNING'

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
