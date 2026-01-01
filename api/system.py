"""
系统监控API
"""

from flask import jsonify, request
from datetime import datetime, timedelta
import psutil
import platform
from app import db
from models.system import SystemStatus
from . import api_v1

@api_v1.route('/system/info', methods=['GET'])
def system_info():
    """获取系统基本信息"""
    try:
        info = {
            'system': {
                'platform': platform.system(),
                'platform_release': platform.release(),
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'hostname': platform.node(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
            },
            'cpu': {
                'cores': psutil.cpu_count(logical=False),
                'logical_cores': psutil.cpu_count(logical=True),
                'usage_percent': psutil.cpu_percent(interval=1),
                'freq_current': psutil.cpu_freq().current if hasattr(psutil.cpu_freq(), 'current') else None,
                'freq_max': psutil.cpu_freq().max if hasattr(psutil.cpu_freq(), 'max') else None,
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'used': psutil.virtual_memory().used,
                'free': psutil.virtual_memory().free,
                'percent': psutil.virtual_memory().percent,
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free,
                'percent': psutil.disk_usage('/').percent,
            },
            'boot_time': psutil.boot_time(),
            'uptime': datetime.now() - datetime.fromtimestamp(psutil.boot_time()),
            'timestamp': datetime.utcnow().isoformat(),
        }
        
        # 获取系统负载
        load = psutil.getloadavg()
        info['load'] = {
            'load_1': load[0],
            'load_5': load[1],
            'load_15': load[2],
        }
        
        return jsonify(info)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/system/metrics', methods=['GET'])
def system_metrics():
    """获取系统指标历史数据"""
    try:
        # 获取查询参数
        hours = request.args.get('hours', default=24, type=int)
        limit = request.args.get('limit', default=100, type=int)
        
        # 计算时间范围
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # 查询数据
        metrics = SystemStatus.query \
            .filter(SystemStatus.timestamp >= since) \
            .order_by(SystemStatus.timestamp.desc()) \
            .limit(limit) \
            .all()
        
        return jsonify({
            'metrics': [m.to_dict() for m in metrics],
            'count': len(metrics),
            'hours': hours,
            'timestamp': datetime.utcnow().isoformat(),
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_v1.route('/system/collect', methods=['POST'])
def collect_metrics():
    """手动收集系统指标"""
    try:
        import psutil
        
        metrics = SystemStatus(
            cpu_percent=psutil.cpu_percent(interval=1),
            cpu_count=psutil.cpu_count(logical=False),
            cpu_freq_current=psutil.cpu_freq().current if hasattr(psutil.cpu_freq(), 'current') else None,
            cpu_freq_max=psutil.cpu_freq().max if hasattr(psutil.cpu_freq(), 'max') else None,
            
            memory_percent=psutil.virtual_memory().percent,
            memory_total=psutil.virtual_memory().total,
            memory_available=psutil.virtual_memory().available,
            memory_used=psutil.virtual_memory().used,
            memory_free=psutil.virtual_memory().free,
            
            disk_percent=psutil.disk_usage('/').percent,
            disk_total=psutil.disk_usage('/').total,
            disk_used=psutil.disk_usage('/').used,
            disk_free=psutil.disk_usage('/').free,
            
            network_sent=psutil.net_io_counters().bytes_sent,
            network_recv=psutil.net_io_counters().bytes_recv,
            
            load_1=psutil.getloadavg()[0],
            load_5=psutil.getloadavg()[1],
            load_15=psutil.getloadavg()[2],
        )
        
        db.session.add(metrics)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '指标收集成功',
            'timestamp': datetime.utcnow().isoformat(),
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
