"""
WSGI入口文件 - 用于生产部署
"""

from app import app

if __name__ == '__main__':
    app.run()
