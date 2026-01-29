#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
产品搜索爬虫应用 - Web界面
"""

import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import (
    init_database, 
    save_search_history, 
    update_search_results,
    get_search_history, 
    get_search_detail,
    delete_search_record
)
from brave_search import search_products

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# 初始化数据库
init_database()

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """执行搜索"""
    try:
        keyword = request.form.get('keyword', '').strip()
        platform = request.form.get('platform', 'Amazon')
        top_n = int(request.form.get('top_n', 10))
        
        if not keyword:
            flash('请输入搜索关键词', 'error')
            return redirect(url_for('index'))
        
        if top_n < 1 or top_n > 20:
            top_n = 10
        
        # 保存搜索记录
        search_id = save_search_history(keyword, platform, top_n)
        
        # 执行搜索
        results = search_products(keyword, platform, top_n)
        
        # 更新结果
        update_search_results(search_id, results)
        
        # 存储搜索ID到session
        # 跳转到结果页面
        
        return redirect(url_for('results', search_id=search_id))
        
    except Exception as e:
        flash(f'搜索出错: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/results/<search_id>')
def results(search_id):
    """搜索结果页面"""
    detail = get_search_detail(search_id)
    
    if not detail:
        flash('未找到该搜索记录', 'error')
        return redirect(url_for('index'))
    
    return render_template('results.html', detail=detail)

@app.route('/history')
def history():
    """搜索历史页面"""
    search_history = get_search_history(limit=50)
    return render_template('history.html', history=search_history)

@app.route('/history/search')
def history_search():
    """搜索历史查询"""
    keyword = request.args.get('keyword', '').strip()
    
    if not keyword:
        return jsonify(get_search_history(20))
    
    results = get_search_history_by_keyword(keyword)
    return jsonify(results)

@app.route('/history/<search_id>')
def history_detail(search_id):
    """历史记录详情"""
    detail = get_search_detail(search_id)
    
    if not detail:
        return jsonify({'error': '未找到记录'}), 404
    
    return jsonify(detail)

@app.route('/history/delete/<search_id>', methods=['POST'])
def delete_history(search_id):
    """删除历史记录"""
    try:
        delete_search_record(search_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def api_search():
    """API接口：执行搜索"""
    try:
        data = request.get_json()
        
        keyword = data.get('keyword', '').strip()
        platform = data.get('platform', 'Amazon')
        top_n = int(data.get('top_n', 10))
        
        if not keyword:
            return jsonify({'error': '请提供搜索关键词'}), 400
        
        # 执行搜索
        search_id = save_search_history(keyword, platform, top_n)
        results = search_products(keyword, platform, top_n)
        update_search_results(search_id, results)
        
        return jsonify({
            'success': True,
            'search_id': search_id,
            'keyword': keyword,
            'platform': platform,
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def api_history():
    """API接口：获取历史"""
    limit = int(request.args.get('limit', 20))
    history = get_search_history(limit)
    return jsonify(history)

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error=error), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error=error), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"产品搜索爬虫应用启动中...")
    print(f"访问地址: http://localhost:{port}")
    print(f"历史记录: http://localhost:{port}/history")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
