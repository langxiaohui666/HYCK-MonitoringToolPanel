#!/usr/bin/env python3
"""
HYCK Monitoring Tool Panel - 主应用文件
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
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
login_manager.login_view = 'api_v1.login'
mail = Mail(app)

# 导入模型（必须在db定义后导入）
from models.user import User

@login_manager.user_loader
def load_user(user_id):
    """用户加载器"""
    return User.query.get(int(user_id))

# 导入API蓝图
from api import api_v1 as api_v1_blueprint
app.register_blueprint(api_v1_blueprint)

# 基础路由
@app.route('/')
def index():
    """首页"""
    return jsonify({
        'name': 'HYCK Monitoring Tool Panel',
        'version': '1.0.0',
        'description': '一个现代化的Linux服务器监控工具面板',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'api_v1': '/api/v1',
            'health': '/api/health',
            'system_info': '/api/v1/system/info',
            'docs': '/docs',  # 未来添加API文档
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    try:
        # 检查数据库连接
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'HYCK Monitoring Panel',
        'database': db_status,
        'version': '1.0.0',
    })

@app.route('/api/version', methods=['GET'])
def version_info():
    """版本信息"""
    return jsonify({
        'name': 'HYCK Monitoring Tool Panel',
        'version': '1.0.0',
        'author': 'HYCK Team',
        'license': 'MIT',
        'repository': 'https://github.com/langxiaohui666/HYCK-Monitoring-Tool-Panel',
        'timestamp': datetime.utcnow().isoformat(),
    })

# 错误处理
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': '资源未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': '服务器内部错误'}), 500

# 启动监控器
@app.before_first_request
def setup_monitoring():
    """启动系统监控"""
    try:
        from utils import Monitor
        monitor = Monitor(interval=app.config.get('MONITOR_INTERVAL', 5))
        monitor.start()
        logger.info("系统监控器已启动")
    except Exception as e:
        logger.error(f"启动监控器失败: {e}")

# 创建数据库表
with app.app_context():
    try:
        db.create_all()
        logger.info("数据库表创建完成")
        
        # 创建默认管理员用户
        from models.user import User
        admin = User.query.filter_by(email='admin@localhost').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@localhost',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            logger.info("默认管理员用户创建完成")
    
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")

if __name__ == '__main__':
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 3000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
