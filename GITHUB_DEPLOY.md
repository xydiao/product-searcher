# GitHub + 云平台一键部署指南

本指南将帮助你把产品搜索应用部署到公网。

## 步骤1：创建GitHub仓库

### 方法1：使用Git命令行
```bash
cd /root/clawd/product_searcher

# 初始化Git
git init
git add .
git commit -m "Initial commit: 产品搜索爬虫应用"

# 创建GitHub仓库（需要在GitHub.com创建空仓库）
git remote add origin https://github.com/你的用户名/product-searcher.git
git branch -M main
git push -u origin main
```

### 方法2：使用GitHub Desktop
1. 下载GitHub Desktop
2. 选择 "Add Local Repository"
3. 选择 `/root/clawd/product_searcher`
4. 点击 "Publish repository"

## 步骤2：部署到Render.com（推荐）

### 2.1 创建Render账号
1. 访问 https://dashboard.render.com
2. 点击 "Sign Up" 注册（可用GitHub账号登录）

### 2.2 部署Web服务
1. 点击 "New +" → "Web Service"
2. 选择你的GitHub仓库
3. 配置：
   - **Name**: `product-searcher`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free（免费）

### 2.3 添加环境变量
在Environment Variables部分添加：
- Key: `BRAVE_API_KEY`
- Value: `你的Brave API Key`

### 2.4 部署
点击 "Create Web Service"

### 2.5 访问应用
部署完成后，Render会提供一个URL，如：
`https://product-searcher.onrender.com`

## 步骤3：部署到Railway（更简单）

### 3.1 创建Railway账号
1. 访问 https://railway.app
2. 点击 "Start Deploying" → "Deploy Now"
3. 用GitHub登录

### 3.2 部署
1. 选择 "Deploy from GitHub repo"
2. 选择你的GitHub仓库
3. Railway会自动检测是Python/Flask应用
4. 添加环境变量：
   - `BRAVE_API_KEY`: 你的API Key
5. 点击 "Deploy"

### 3.3 访问
Railway会提供一个随机域名，如：
`https://product-searcher-production.up.railway.app`

## 步骤4：自定义域名（可选）

### Render自定义域名：
1. 在Render Dashboard中点击你的服务
2. 找到 "Custom Domains"
3. 添加你的域名
4. 按照提示配置DNS

### Railway自定义域名：
1. 在项目Settings中找到 "Domains"
2. 添加你的域名
3. 配置CNAME记录

## 常见问题

### Q: 部署失败怎么办？
A: 
1. 检查GitHub Actions日志
2. 确保requirements.txt中的依赖正确
3. 查看Render/Railway的部署日志

### Q: 如何更新应用？
A: 
```bash
# 本地更新代码
git add .
git commit -m "Update"
git push

# Render/Railway会自动重新部署
```

### Q: 免费版有什么限制？
A: 
- Render: 每月750小时运行时间
- Railway: 每月500小时运行时间
- 空闲时会休眠，访问时自动唤醒

## 配置HTTPS

所有云平台都自动提供SSL证书，访问地址默认是HTTPS。

## 监控和日志

- Render: Dashboard → 你的服务 → Logs
- Railway: Project → Deployments → 查看日志

## 成本

✅ **免费**：
- Render: 750小时/月
- Railway: 500小时/月
- 自动HTTPS
- 自定义域名

💰 **付费**（可选）：
- 更多运行时间
- 自定义域名
- 私有仓库

## 快速对比

| 特性 | Render | Railway |
|------|--------|---------|
| 免费额度 | 750小时/月 | 500小时/月 |
| 自动HTTPS | ✅ | ✅ |
| 自定义域名 | ✅ | ✅ |
| 部署难度 | ⭐⭐ | ⭐ |
| 速度 | ⭐⭐⭐ | ⭐⭐⭐ |
| 稳定性 | ⭐⭐⭐ | ⭐⭐⭐ |

## 下一步

1. 将代码推送到GitHub
2. 选择一个平台部署
3. 分享你的应用URL！

## 技术支持

遇到问题？
1. 查看平台官方文档
2. 检查部署日志
3. 搜索错误信息

祝部署顺利！🚀
