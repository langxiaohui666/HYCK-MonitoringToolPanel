"""
API接口包
"""
from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# 导入路由
from . import system, process, network, disk, docker, auth

__all__ = ['api_v1']
