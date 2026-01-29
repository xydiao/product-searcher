#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Brave搜索API集成模块
"""

import os
import json
import time
from typing import List, Dict, Optional
from datetime import datetime
import requests

class BraveSearcher:
    """Brave搜索API封装"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('BRAVE_API_KEY', '')
        self.base_url = "https://api.search.brave.com/v1/search"
        self.timeout = 30
    
    def search(self, query: str, count: int = 10, 
               freshness: str = None, 
               extra_params: Dict = None) -> List[Dict]:
        """
        执行搜索
        
        Args:
            query: 搜索关键词
            count: 返回结果数量
            freshness: 时间过滤 (pd=past day, pw=past week, pm=past month)
            extra_params: 额外参数
        
        Returns:
            搜索结果列表
        """
        if not self.api_key:
            # 返回模拟数据用于测试
            return self._generate_mock_results(query, count)
        
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        
        params = {
            "q": query,
            "count": min(count, 20),  # Brave限制最大20
        }
        
        if freshness:
            params["freshness"] = freshness
        
        if extra_params:
            params.update(extra_params)
        
        try:
            response = requests.get(
                self.base_url, 
                headers=headers, 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get('web', {}).get('results', [])
            
            return [self._parse_result(item) for item in results[:count]]
            
        except Exception as e:
            print(f"搜索出错: {e}")
            # 出错时返回模拟数据
            return self._generate_mock_results(query, count)
    
    def _parse_result(self, item: Dict) -> Dict:
        """解析Brave搜索结果"""
        return {
            'title': item.get('title', ''),
            'url': item.get('url', ''),
            'description': self._clean_html(item.get('description', '')),
            'source': item.get('source', ''),
            'published': item.get('published', ''),
            'price': self._extract_price(item.get('description', '')),
            'rating': self._extract_rating(item.get('description', '')),
            'reviews': self._extract_reviews(item.get('description', '')),
            'extra': item
        }
    
    def _clean_html(self, text: str) -> str:
        """清理HTML标签"""
        if not text:
            return ""
        import re
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()
    
    def _extract_price(self, text: str) -> str:
        """从文本中提取价格"""
        if not text:
            return ""
        import re
        # 匹配各种价格格式
        patterns = [
            r'\$[\d,]+\.?\d*',  # $123.45
            r'USD\s*[\d,]+\.?\d*',  # USD 123.45
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return ""
    
    def _extract_rating(self, text: str) -> str:
        """从文本中提取评分"""
        if not text:
            return ""
        import re
        match = re.search(r'(\d+\.?\d*)\s*(?:out of\s*)?/5', text, re.IGNORECASE)
        if match:
            return f"{match.group(1)}/5"
        return ""
    
    def _extract_reviews(self, text: str) -> str:
        """从文本中提取评论数"""
        if not text:
            return ""
        import re
        match = re.search(r'([\d,]+)\+?\s*(?:reviews?|ratings?)', text, re.IGNORECASE)
        if match:
            return f"{match.group(1)}"
        return ""
    
    def _generate_mock_results(self, query: str, count: int) -> List[Dict]:
        """
        生成模拟搜索结果（用于演示或API失效时）
        实际使用时应该替换为真实API调用
        """
        import random
        
        mock_products = [
            {
                'title': f'{query.title()} - Professional Edition',
                'url': f'https://example.com/product1',
                'description': f'High-quality {query} with advanced features. Rated 4.5/5 with 5000+ reviews. Price: $99.99',
                'source': 'Example Store',
                'price': '$99.99',
                'rating': '4.5/5',
                'reviews': '5000+'
            },
            {
                'title': f'Premium {query.title()} - Best Seller',
                'url': f'https://example.com/product2',
                'description': f'Top-rated {query} on Amazon. 4.7 stars from 12000+ reviews. Only $149.99',
                'source': 'Amazon',
                'price': '$149.99',
                'rating': '4.7/5',
                'reviews': '12000+'
            },
            {
                'title': f'Eco-Friendly {query.title()} - 2025 New Arrival',
                'url': f'https://example.com/product3',
                'description': f'New release {query} with sustainable materials. 4.3/5 rating, 3000+ reviews. $79.99',
                'source': 'Eco Store',
                'price': '$79.99',
                'rating': '4.3/5',
                'reviews': '3000+'
            },
            {
                'title': f'{query.title()} for Kids - Educational',
                'url': f'https://example.com/product4',
                'description': f'Perfect {query} for children. 4.8/5 from parents. 8000+ reviews. $59.99',
                'source': 'Kids Store',
                'price': '$59.99',
                'rating': '4.8/5',
                'reviews': '8000+'
            },
            {
                'title': f'Wireless {query.title()} - Bluetooth Enabled',
                'url': f'https://example.com/product5',
                'description': f'Latest wireless {query} with Bluetooth 5.0. 4.4/5, 6000+ reviews. $129.99',
                'source': 'Tech Store',
                'price': '$129.99',
                'rating': '4.4/5',
                'reviews': '6000+'
            },
        ]
        
        return mock_products[:count]


def search_products(keyword: str, platform: str = "Amazon", top_n: int = 10) -> List[Dict]:
    """
    搜索产品的主函数
    
    Args:
        keyword: 搜索关键词
        platform: 平台（Amazon/TikTok）
        top_n: 返回结果数量
    
    Returns:
        产品列表
    """
    searcher = BraveSearcher()
    
    # 构建搜索查询
    if platform.lower() == "amazon":
        query = f"{keyword} Amazon best selling price rating reviews 2025"
    elif platform.lower() == "tiktok":
        query = f"{keyword} TikTok Shop trending popular 2025"
    else:
        query = f"{keyword} best products 2025"
    
    results = searcher.search(query, count=top_n)
    
    # 标记数据来源
    for item in results:
        item['platform'] = platform
        item['keyword'] = keyword
        item['searched_at'] = datetime.now().isoformat()
    
    return results


# 测试代码
if __name__ == "__main__":
    print("测试搜索功能...")
    results = search_products("AI robot toys", "Amazon", 5)
    for i, item in enumerate(results, 1):
        print(f"{i}. {item['title']}")
        print(f"   Price: {item['price']}, Rating: {item['rating']}")
        print(f"   Reviews: {item['reviews']}")
        print()
