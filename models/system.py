"""
系统监控数据模型
"""

from datetime import datetime
from app import db

class SystemStatus(db.Model):
    """系统状态记录"""
    __tablename__ = 'system_status'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # CPU信息
    cpu_percent = db.Column(db.Float)
    cpu_count = db.Column(db.Integer)
    cpu_freq_current = db.Column(db.Float)
    cpu_freq_max = db.Column(db.Float)
    
    # 内存信息
    memory_percent = db.Column(db.Float)
    memory_total = db.Column(db.BigInteger)  # bytes
    memory_available = db.Column(db.BigInteger)
    memory_used = db.Column(db.BigInteger)
    memory_free = db.Column(db.BigInteger)
    
    # 磁盘信息
    disk_percent = db.Column(db.Float)
    disk_total = db.Column(db.BigInteger)
    disk_used = db.Column(db.BigInteger)
    disk_free = db.Column(db.BigInteger)
    
    # 网络信息
    network_sent = db.Column(db.BigInteger)  # bytes
    network_recv = db.Column(db.BigInteger)
    
    # 系统负载
    load_1 = db.Column(db.Float)
    load_5 = db.Column(db.Float)
    load_15 = db.Column(db.Float)
    
    # 温度（如果可用）
    cpu_temp = db.Column(db.Float)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'cpu': {
                'percent': self.cpu_percent,
                'count': self.cpu_count,
                'freq_current': self.cpu_freq_current,
                'freq_max': self.cpu_freq_max,
            },
            'memory': {
                'percent': self.memory_percent,
                'total': self.memory_total,
                'available': self.memory_available,
                'used': self.memory_used,
                'free': self.memory_free,
            },
            'disk': {
                'percent': self.disk_percent,
                'total': self.disk_total,
                'used': self.disk_used,
                'free': self.disk_free,
            },
            'network': {
                'sent': self.network_sent,
                'recv': self.network_recv,
            },
            'load': {
                'load_1': self.load_1,
                'load_5': self.load_5,
                'load_15': self.load_15,
            },
            'cpu_temp': self.cpu_temp,
        }

class MonitorEvent(db.Model):
    """监控事件记录"""
    __tablename__ = 'monitor_events'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    event_type = db.Column(db.String(50))  # alert, info, warning, error
    severity = db.Column(db.String(20))    # low, medium, high, critical
    source = db.Column(db.String(50))      # cpu, memory, disk, network, system
    message = db.Column(db.Text)
    details = db.Column(db.JSON)
    resolved = db.Column(db.Boolean, default=False)
    resolved_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<MonitorEvent {self.event_type} - {self.severity}>'
