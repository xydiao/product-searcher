#!/bin/bash
# 启动脚本

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 初始化数据库
echo "初始化数据库..."
python -c "from database import init_database; init_database()"

# 启动应用
echo "启动Web应用..."
export DEBUG=${DEBUG:-False}
python app.py
