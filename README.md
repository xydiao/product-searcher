# 产品搜索爬虫应用

一个支持多平台产品搜索的Web应用，自动保存搜索记录。

## 功能特点

✅ 支持亚马逊、TikTok等多平台搜索  
✅ 实时Brave API搜索集成  
✅ 自动保存搜索历史  
✅ CSV格式数据导出  
✅ 响应式Web界面  
✅ RESTful API接口

## 快速开始

### 1. 安装依赖

```bash
cd /root/clawd/product_searcher
pip install -r requirements.txt
```

### 2. 配置Brave API Key

在环境变量中设置：
```bash
export BRAVE_API_KEY="your_api_key_here"
```

或在 `brave_search.py` 中直接修改：
```python
def __init__(self, api_key: str = "your_api_key_here"):
```

### 3. 启动应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动

### 4. 使用Docker

```bash
docker build -t product-searcher .
docker run -p 5000:5000 -e BRAVE_API_KEY="your_key" product-searcher
```

## Web界面使用

1. 访问 `http://localhost:5000`
2. 输入搜索关键词
3. 选择搜索平台（Amazon/TikTok）
4. 选择返回结果数量
5. 点击"开始搜索"
6. 查看结果并可导出CSV

## API接口

### 执行搜索
```bash
POST /api/search
Content-Type: application/json

{
    "keyword": "AI robot toys",
    "platform": "Amazon",
    "top_n": 10
}
```

### 获取历史
```bash
GET /api/history?limit=20
```

## 目录结构

```
product_searcher/
├── app.py              # Flask主应用
├── database.py         # 数据库操作
├── brave_search.py     # Brave搜索API
├── requirements.txt    # Python依赖
├── start.sh           # 启动脚本
├── Dockerfile         # Docker配置
├── README.md          # 说明文档
├── static/
│   └── css/
│       └── style.css  # 样式文件
└── templates/
    ├── index.html     # 首页
    ├── results.html   # 结果页
    ├── history.html   # 历史页
    └── error.html     # 错误页
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| BRAVE_API_KEY | Brave搜索API密钥 | - |
| PORT | Web服务端口 | 5000 |
| DEBUG | 调试模式 | False |

## 数据存储

搜索历史保存在 SQLite 数据库中：
- 路径：`/root/clawd/product_searcher/search_history.db`
- 自动记录搜索关键词、时间、平台、结果

## 注意事项

⚠️ 本应用仅用于学习和研究目的  
⚠️ 请遵守各平台的robots.txt和使用条款  
⚠️ 搜索结果仅供参考，不构成购买建议

## 许可证

MIT License
