# <img src="images/logo.png" width="40" height="40" align="right" /> HYCK Monitoring Tool Panel

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)

**一个现代化、轻量级的 Linux 服务器监控工具面板**  
**基于 Python，适用于 VPS / 云服务器 / 宝塔面板**

[📚 使用文档](#-快速开始) ·
[📸 界面预览](#-界面预览) ·
[🐛 问题反馈](https://github.com/langxiaohui666/HYCK-Monitoring-Tool-Panel/issues)

</div>

---

## ✨ 项目特性

### 📊 系统监控
- CPU / 内存 / 磁盘 / 网络信息采集
- 服务器运行状态概览
- 低资源占用，适合小内存 VPS

### 🔧 后端能力
- Python 后端架构，代码清晰
- API 模块化设计，便于扩展
- 支持数据库初始化脚本

### 🎨 项目风格
- 简洁现代，专注功能本身
- 适合二次开发为完整监控面板
- README 与代码结构完全一致

### 🔒 安全性
- 使用 `.env` 管理敏感配置
- 可部署于内网或公网
- 支持 Nginx 反向代理

---

## 📁 项目结构

```text
HYCK-Monitoring-Tool-Panel/
├── api/                    # API 接口
├── config/                 # 配置文件
├── images/                 # README 图片资源
├── main/                   # 主程序目录
│   ├── app.py              # 应用入口
│   ├── config.py           # 主配置文件
│   ├── requirements.txt    # Python 依赖
│   └── wsgi.py
├── models/                 # 数据模型
├── scripts/                # 脚
