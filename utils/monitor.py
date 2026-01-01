"""
监控工具类
"""

import psutil
import platform
import socket
from datetime import datetime
from threading import Thread, Event
import time
import logging

logger = logging.getLogger(__name__)

class Monitor:
    """系统监控器"""
    
    def __init__(self, interval=5):
        self.interval = interval
        self.is_running = False
        self.thread = None
        self.stop_event = Event()
        
    def start(self):
        """启动监控"""
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self.thread = Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            logger.info(f"监控器已启动，间隔: {self.interval}秒")
    
    def stop(self):
        """停止监控"""
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            if self.thread:
                self.thread.join(timeout=5)
            logger.info("监控器已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while not self.stop_event.is_set():
            try:
                self.collect_metrics()
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"监控循环错误: {e}")
                time.sleep(1)
    
    def collect_metrics(self):
        """收集系统指标"""
        try:
            metrics = {
                'timestamp': datetime.utcnow(),
                'cpu': self.get_cpu_info(),
                'memory': self.get_memory_info(),
                'disk': self.get_disk_info(),
                'network': self.get_network_info(),
                'system': self.get_system_info(),
            }
            
            # 这里可以保存到数据库或发送到其他地方
            logger.debug(f"收集指标: CPU={metrics['cpu']['percent']}%, Memory={metrics['memory']['percent']}%")
            
            return metrics
            
        except Exception as e:
            logger.error(f"收集指标失败: {e}")
            return None
    
    def get_cpu_info(self):
        """获取CPU信息"""
        return {
            'percent': psutil.cpu_percent(interval=0.1),
            'count': psutil.cpu_count(logical=False),
            'logical_count': psutil.cpu_count(logical=True),
            'freq_current': psutil.cpu_freq().current if hasattr(psutil.cpu_freq(), 'current') else None,
            'freq_max': psutil.cpu_freq().max if hasattr(psutil.cpu_freq(), 'max') else None,
            'load_avg': psutil.getloadavg(),
        }
    
    def get_memory_info(self):
        """获取内存信息"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'free': mem.free,
            'percent': mem.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_free': swap.free,
            'swap_percent': swap.percent,
        }
    
    def get_disk_info(self):
        """获取磁盘信息"""
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent,
                })
            except (PermissionError, FileNotFoundError):
                continue
        
        disk_io = psutil.disk_io_counters()
        
        return {
            'partitions': partitions,
            'io_counters': {
                'read_count': disk_io.read_count if disk_io else None,
                'write_count': disk_io.write_count if disk_io else None,
                'read_bytes': disk_io.read_bytes if disk_io else None,
                'write_bytes': disk_io.write_bytes if disk_io else None,
            } if disk_io else None,
        }
    
    def get_network_info(self):
        """获取网络信息"""
        net_io = psutil.net_io_counters()
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        interfaces = {}
        for interface, addrs in net_if_addrs.items():
            interfaces[interface] = {
                'addresses': [
                    {
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast,
                    }
                    for addr in addrs
                ],
                'stats': net_if_stats.get(interface, {})._asdict() 
                if interface in net_if_stats else None,
            }
        
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'interfaces': interfaces,
        }
    
    def get_system_info(self):
        """获取系统信息"""
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
            'processor': platform.processor(),
            'boot_time': psutil.boot_time(),
            'users': len(psutil.users()),
            'uptime': time.time() - psutil.boot_time(),
        }
