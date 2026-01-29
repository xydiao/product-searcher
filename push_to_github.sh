#!/bin/bash
# 推送到GitHub的脚本

set -e

echo "🚀 开始推送到GitHub..."

# 检查git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装"
    exit 1
fi

cd /root/clawd/product_searcher

# 初始化git仓库（如果尚未初始化）
if [ ! -d .git ]; then
    echo "📦 初始化Git仓库..."
    git init
    git add .
    git commit -m "Initial commit: 产品搜索爬虫应用

功能特点：
- 支持多平台搜索（亚马逊、TikTok）
- 自动保存搜索历史
- 美观的Web界面
- RESTful API接口
- CSV数据导出

包含文件：
- Flask Web应用
- SQLite数据库
- Brave Search API集成
- 响应式前端界面

Created by 墨智云图 🧠"
else
    echo "✅ Git仓库已存在"
fi

echo ""
echo "📝 下一步操作："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  创建GitHub访问令牌："
echo "   访问：https://github.com/settings/tokens"
echo "   点击 'Generate new token (classic)'"
echo "   配置："
echo "   - Note: product-searcher-deploy"
echo "   - Expiration: 90 days"
echo "   - 勾选: 'repo' (完全控制私有仓库)"
echo "   - 点击 'Generate token'"
echo "   - 复制生成的token（格式：ghp_xxxxxxxxxxxx）"
echo ""
echo "2️⃣  在这里运行："
echo "   git remote set-url origin https://[TOKEN]@github.com/用户名/仓库名.git"
echo "   git push -u origin main"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 提示："
echo "- 用户名：你注册GitHub时用的用户名"
echo "- 仓库名：可以设为 'product-searcher'"
echo "- Token只显示一次，请立即复制保存！"
echo ""
echo "需要我继续协助吗？"
