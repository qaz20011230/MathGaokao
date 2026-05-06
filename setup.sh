#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================"
echo "  mathgaokao.top 开发环境启动"
echo "========================================"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

echo ""
echo "[1/4] 检查 Node.js..."
if ! command -v node &>/dev/null; then
    echo "  Node.js 未安装，请先安装 v18+"
    exit 1
fi
echo "  Node.js $(node --version) ✓"

echo ""
echo "[2/4] 检查 MySQL..."
if ! command -v mysql &>/dev/null; then
    echo "  MySQL 未安装"
    echo "  选项 A: brew install mysql && brew services start mysql"
    echo "  选项 B: docker compose up mysql -d"
    echo "  请先启动 MySQL 服务，然后继续"
    exit 1
fi
echo "  MySQL ✓"

echo ""
echo "[3/4] 安装前端依赖..."
cd "$PROJECT_DIR/frontend"
npm install --silent 2>&1 | tail -1
echo "  前端依赖 ✓"

echo ""
echo "[4/4] 安装后端依赖..."
cd "$PROJECT_DIR/backend"
pip3 install --user -q -r requirements.txt 2>&1 | tail -1
echo "  后端依赖 ✓"

echo ""
echo "========================================"
echo "  初始化数据库..."
echo "========================================"
echo ""

export PATH="$HOME/Library/Python/3.9/bin:$PATH"

cd "$PROJECT_DIR/backend"
python3 -c "
import sys; sys.path.insert(0, '.')
from app.database import engine, Base
from app.models.document import Document, Admin
Base.metadata.create_all(bind=engine)
print('数据库表创建完成')
"

python3 seeds/seed_1977_2025.py

echo ""
echo "========================================"
echo "  启动服务"
echo "========================================"
echo ""
echo "  在另一个终端中运行:"
echo "    后端: cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo "    前端: cd frontend && npm run dev"
echo ""
echo "  访问:"
echo "    前台: http://localhost:3000"
echo "    后台: http://localhost:3000/admin"
echo "    API:  http://localhost:8000/api/health"
echo "========================================"
