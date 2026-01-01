#!/usr/bin/env python3
"""
数据库初始化脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✅ 数据库表创建完成")
        
        # 创建默认管理员用户
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
            print("✅ 默认管理员用户创建完成")
            print("   用户名: admin")
            print("   密码: admin123")
        else:
            print("ℹ️  管理员用户已存在")
        
        print("\n🎉 数据库初始化完成！")

if __name__ == '__main__':
    init_database()
