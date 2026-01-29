#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库操作模块 - 搜索记录存储
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from contextlib import contextmanager

DATABASE_PATH = "/root/clawd/product_searcher/search_history.db"

@contextmanager
def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """初始化数据库表"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 创建搜索记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id TEXT UNIQUE NOT NULL,
                keyword TEXT NOT NULL,
                platform TEXT NOT NULL,
                top_n INTEGER DEFAULT 10,
                results TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT (datetime('now')),
                completed_at TEXT
            )
        ''')
        
        # 创建搜索详情表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id TEXT NOT NULL,
                rank INTEGER,
                title TEXT,
                url TEXT,
                description TEXT,
                price TEXT,
                rating TEXT,
                reviews TEXT,
                source TEXT,
                data_json TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (search_id) REFERENCES search_history(search_id)
            )
        ''')
        
        conn.commit()
    print("数据库初始化完成")

def save_search_history(keyword: str, platform: str, top_n: int) -> str:
    """保存搜索记录，返回search_id"""
    import uuid
    search_id = str(uuid.uuid4())[:8]
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO search_history (search_id, keyword, platform, top_n, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (search_id, keyword, platform, top_n))
        conn.commit()
    
    return search_id

def update_search_results(search_id: str, results: List[Dict], status: str = 'completed'):
    """更新搜索结果"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 更新搜索状态
        cursor.execute('''
            UPDATE search_history 
            SET results = ?, status = ?, completed_at = ?
            WHERE search_id = ?
        ''', (json.dumps(results, ensure_ascii=False), status, datetime.now(), search_id))
        
        # 保存详细结果
        for idx, item in enumerate(results, 1):
            cursor.execute('''
                INSERT INTO search_details 
                (search_id, rank, title, url, description, price, rating, reviews, source, data_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                search_id,
                idx,
                item.get('title', ''),
                item.get('url', ''),
                item.get('description', ''),
                item.get('price', ''),
                item.get('rating', ''),
                item.get('reviews', ''),
                item.get('source', ''),
                json.dumps(item, ensure_ascii=False)
            ))
        
        conn.commit()

def get_search_history(limit: int = 20) -> List[Dict]:
    """获取搜索历史"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM search_history 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_search_detail(search_id: str) -> Optional[Dict]:
    """获取单次搜索的详细信息"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 获取搜索记录
        cursor.execute('SELECT * FROM search_history WHERE search_id = ?', (search_id,))
        search = cursor.fetchone()
        
        if not search:
            return None
        
        # 获取详细结果
        cursor.execute('SELECT * FROM search_details WHERE search_id = ? ORDER BY rank', (search_id,))
        details = cursor.fetchall()
        
        result = dict(search)
        result['details'] = [dict(row) for row in details]
        return result

def delete_search_record(search_id: str) -> bool:
    """删除搜索记录"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM search_details WHERE search_id = ?', (search_id,))
        cursor.execute('DELETE FROM search_history WHERE search_id = ?', (search_id,))
        conn.commit()
        return True

def search_history_by_keyword(keyword: str) -> List[Dict]:
    """按关键词搜索历史记录"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM search_history 
            WHERE keyword LIKE ? 
            ORDER BY created_at DESC
        ''', (f'%{keyword}%',))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

# 初始化数据库
if __name__ == "__main__":
    init_database()
    print("数据库就绪")
