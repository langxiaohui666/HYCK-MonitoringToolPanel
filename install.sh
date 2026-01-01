#!/bin/bash
set -e

echo "=========================================="
echo "     HYCK监控面板安装脚本 v1.0.0"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 安装目录
INSTALL_DIR="/opt/hyck-monitor"

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# 检查root权限
check_root() {
    if [ "$EUID" -ne 0 ]; then 
        print_error "请使用root权限运行此脚本"
        echo "使用: sudo bash install.sh"
        exit 1
    fi
}

# 检查系统
check_system() {
    print_info "检查系统环境..."
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | awk '{print $2}')
        print_success "Python版本: $PYTHON_VERSION"
    else
        print_error "未找到Python3，请先安装Python3"
        exit 1
    fi
    
    # 检查pip
    if command -v pip3 &> /dev/null; then
        print_success "pip3已安装"
    else
        print_info "安装pip3..."
        apt update && apt install -y python3-pip || yum install -y python3-pip
    fi
}

# 安装依赖
install_dependencies() {
    print_info "安装系统依赖..."
    
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        apt update
        apt install -y \
            python3-venv \
            python3-dev \
            build-essential \
            libssl-dev \
            libffi-dev \
            git \
            curl \
            wget
    elif [ -f /etc/redhat-release ]; then
        # CentOS/RHEL
        yum install -y \
            python3-devel \
            gcc \
            make \
            openssl-devel \
            libffi-devel \
            git \
            curl \
            wget
    else
        print_error "不支持的操作系统"
        exit 1
    fi
}

# 创建目录
create_directories() {
    print_info "创建安装目录..."
    
    mkdir -p $INSTALL_DIR
    mkdir -p $INSTALL_DIR/logs
    mkdir -p $INSTALL_DIR/data
    mkdir -p $INSTALL_DIR/backups
    
    print_success "目录创建完成"
}

# 复制文件
copy_files() {
    print_info "复制文件..."
    
    # 复制当前目录文件
    cp -r ./* $INSTALL_DIR/
    
    # 创建venv
    python3 -m venv $INSTALL_DIR/venv
    
    print_success "文件复制完成"
}

# 安装Python依赖
install_python_packages() {
    print_info "安装Python依赖包..."
    
    source $INSTALL_DIR/venv/bin/activate
    pip install --upgrade pip
    pip install -r $INSTALL_DIR/requirements.txt
    
    print_success "Python依赖安装完成"
}

# 创建配置文件
create_config() {
    print_info "创建配置文件..."
    
    if [ ! -f $INSTALL_DIR/.env ]; then
        cp $INSTALL_DIR/.env.example $INSTALL_DIR/.env
        SECRET_KEY=$(openssl rand -hex 32)
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" $INSTALL_DIR/.env
        print_success "配置文件已创建，请编辑 $INSTALL_DIR/.env 进行配置"
    else
        print_info "配置文件已存在"
    fi
}

# 初始化数据库
init_database() {
    print_info "初始化数据库..."
    
    cd $INSTALL_DIR
    source venv/bin/activate
    python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('数据库创建完成')
"
    
    print_success "数据库初始化完成"
}

# 创建系统服务
create_service() {
    print_info "创建系统服务..."
    
    cat > /etc/systemd/system/hyck-monitor.service << EOF
[Unit]
Description=HYCK Monitoring Tool Panel
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
EnvironmentFile=$INSTALL_DIR/.env
ExecStart=$INSTALL_DIR/venv/bin/gunicorn \
    --bind 0.0.0.0:3000 \
    --workers 4 \
    --threads 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile $INSTALL_DIR/logs/access.log \
    --error-logfile $INSTALL_DIR/logs/error.log \
    app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable hyck-monitor
    systemctl start hyck-monitor
    
    print_success "系统服务创建完成"
}

# 显示安装信息
show_installation_info() {
    echo ""
    echo "=========================================="
    echo "          安装完成！🎉"
    echo "=========================================="
    echo ""
    echo "安装目录: $INSTALL_DIR"
    echo "服务端口: 3000"
    echo ""
    echo "管理命令:"
    echo "  启动服务: sudo systemctl start hyck-monitor"
    echo "  停止服务: sudo systemctl stop hyck-monitor"
    echo "  重启服务: sudo systemctl restart hyck-monitor"
    echo "  查看状态: sudo systemctl status hyck-monitor"
    echo "  查看日志: sudo journalctl -u hyck-monitor -f"
    echo ""
    echo "访问地址:"
    echo "  http://您的服务器IP:3000"
    echo ""
    echo "默认登录信息:"
    echo "  用户名: admin"
    echo "  密码: admin123"
    echo ""
    echo "请确保已配置防火墙允许3000端口访问"
    echo "=========================================="
}

# 主函数
main() {
    check_root
    check_system
    install_dependencies
    create_directories
    copy_files
    install_python_packages
    create_config
    init_database
    create_service
    
    print_success "HYCK监控面板安装完成！"
    show_installation_info
}

# 运行主函数
main "$@"
