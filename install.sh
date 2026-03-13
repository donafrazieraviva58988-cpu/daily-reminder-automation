#!/bin/bash

# 每日提醒自动化 - 一键安装脚本

echo "=================================="
echo "  每日提醒自动化 - 安装脚本"
echo "=================================="

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装"
    exit 1
fi

echo "✅ Python3 已安装: $(python3 --version)"

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip3 install pyobjc-framework-EventKit

# 检查权限
echo ""
echo "🔐 首次运行时，请授权以下权限："
echo "   1. 提醒事项访问权限"
echo "   2. 终端权限"
echo ""
echo "   路径：系统设置 → 隐私与安全性 → 提醒事项"

# 测试
echo ""
echo "🧪 测试安装..."
python3 -c "from EventKit import EKEventStore; print('✅ EventKit 可用')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "  ✅ 安装完成！"
    echo "=================================="
    echo ""
    echo "📖 使用方法："
    echo ""
    echo "  python3 scripts/create_reminder.py '配置JSON'"
    echo ""
    echo "  或使用示例："
    echo "  python3 scripts/create_reminder.py examples/config.json"
    echo ""
else
    echo ""
    echo "❌ 安装失败，请检查错误信息"
fi
