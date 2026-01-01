#!/bin/bash
set -e

echo ""
echo "=========================================="
echo "    HYCK Monitoring Tool Panel 安装程序"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 解析参数
INSTALL_PATH="/opt/hyck-monitor"
PORT="3000"

while [[ $# -gt 0 ]]; do
    case $1 in
        --path)
            INSTALL_PATH="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# 检查系统
check_system() {
    print_info "检查系统环境..."
    
    if ! command -v python3 &>/dev/null; then
        print_error "未找到Python3"
        echo "请先安装Python3:"
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    print_success "Python版本: $PYTHON_VERSION"
}

# 安装依赖
install_dependencies() {
    print_info "安装系统依赖..."
    
    if [ -f /etc/debian_version ]; then
        apt update
        apt install -y python3-venv python3-pip python3-dev git curl wget
    elif [ -f /etc/redhat-release ]; then
        yum install -y python3 python3-pip python3-devel git curl wget
    else
        print_warning "未知系统，尝试使用pip安装..."
    fi
}

# 创建安装目录
create_directories() {
    print_info "创建安装目录: $INSTALL_PATH"
    
    mkdir -p "$INSTALL_PATH"
    mkdir -p "$INSTALL_PATH/logs"
    mkdir -p "$INSTALL_PATH/data"
    
    print_success "目录创建完成"
}

# 复制文件
copy_files() {
    print_info "复制文件..."
    
    # 获取当前脚本目录
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
    
    # 复制所有文件
    cp -r "$PROJECT_DIR"/* "$INSTALL_PATH/" || true
    
    print_success "文件复制完成"
}

# 安装Python依赖
install_python_deps() {
    print_info "安装Python依赖..."
    
    cd "$INSTALL_PATH"
    
    # 创建虚拟环境
    python3 -m venv venv
    source venv/bin/activate
    
    # 升级pip并安装依赖
    pip install --upgrade pip
    pip install -r requirements.txt
    
    print_success "Python依赖安装完成"
}

# 创建配置文件
create_config() {
    print_info "创建配置文件..."
    
    cd "$INSTALL_PATH"
    
    if [ ! -f .env ]; then
        cp .env.example .env
        SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
        sed -i "s/PORT=.*/PORT=$PORT/" .env
        print_success "配置文件已创建"
    else
        print_info "配置文件已存在，跳过创建"
    fi
}

# 初始化数据库
init_database() {
    print_info "初始化数据库..."
    
    cd "$INSTALL_PATH"
    source venv/bin/activate
    
    python3 -c "
from app import app, db, User
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@localhost', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('数据库初始化完成')
"
    
    print_success "数据库初始化完成"
}

# 创建系统服务
create_service() {
    print_info "创建系统服务..."
    
    SERVICE_FILE="/etc/systemd/system/hyck-monitor.service"
    
    cat > $SERVICE_FILE << EOF
[Unit]
Description=HYCK Monitoring Tool Panel
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_PATH
Environment="PATH=$INSTALL_PATH/venv/bin"
EnvironmentFile=$INSTALL_PATH/.env
ExecStart=$INSTALL_PATH/venv/bin/gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --log-level info \
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
    echo "          安装完成！ 🎉"
    echo "=========================================="
    echo ""
    echo "安装路径: $INSTALL_PATH"
    echo "服务端口: $PORT"
    echo ""
    echo "管理命令:"
    echo "  sudo systemctl start hyck-monitor"
    echo "  sudo systemctl stop hyck-monitor"
    echo "  sudo systemctl restart hyck-monitor"
    echo "  sudo systemctl status hyck-monitor"
    echo ""
    echo "访问地址:"
    echo "  http://你的服务器IP:$PORT"
    echo ""
    echo "默认登录信息:"
    echo "  用户名: admin"
    echo "  密码: admin123"
    echo ""
    echo "测试服务:"
    echo "  curl http://localhost:$PORT/api/health"
    echo ""
    echo "=========================================="
}

# 主安装流程
main() {
    check_system
    install_dependencies
    create_directories
    copy_files
    install_python_deps
    create_config
    init_database
    create_service
    
    print_success "HYCK监控面板安装完成！"
    show_installation_info
}

# 运行安装
main
