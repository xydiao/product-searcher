#!/usr/bin/env python3
"""
一键启动脚本 - 自动安装依赖并启动服务
"""

import os
import sys
import subprocess
import webbrowser
from threading import Timer

def install_requirements():
    """安装Python依赖"""
    print("📦 安装Python依赖...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ 依赖安装成功")
            return True
        else:
            print(f"❌ 依赖安装失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 安装出错: {e}")
        return False

def init_database():
    """初始化数据库"""
    print("🗄️ 初始化数据库...")
    try:
        from database import init_database
        init_database()
        print("✅ 数据库就绪")
        return True
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

def open_browser():
    """自动打开浏览器"""
    webbrowser.open('http://localhost:5000')

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 产品搜索爬虫应用启动器")
    print("=" * 60)
    
    # 切换到应用目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 安装依赖
    if not install_requirements():
        print("\n请手动安装依赖后重试")
        sys.exit(1)
    
    # 初始化数据库
    if not init_database():
        print("\n数据库初始化失败，但可以继续尝试启动...")
    
    # 提示用户配置API Key
    api_key = os.environ.get('BRAVE_API_KEY', '')
    if not api_key:
        print("\n⚠️  未检测到 BRAVE_API_KEY 环境变量")
        print("   搜索功能将使用模拟数据")
        print("   如需真实数据，请设置环境变量：")
        print("   export BRAVE_API_KEY='your_api_key'")
        print("")
    
    # 启动浏览器
    print("🌐 将在3秒后打开浏览器...")
    Timer(3, open_browser).start()
    
    # 启动应用
    print("\n" + "=" * 60)
    print("🎉 启动应用...")
    print("📍 访问地址: http://localhost:5000")
    print("📚 历史记录: http://localhost:5000/history")
    print("=" * 60 + "\n")
    
    # 启动Flask应用
    os.execv(sys.executable, [sys.executable, "app.py"])

if __name__ == "__main__":
    main()
