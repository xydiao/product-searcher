# 部署清单 - 产品搜索爬虫应用

## ✅ 部署前检查

- [ ] Brave API Key 已准备好
- [ ] GitHub账号已注册
- [ ] 代码已推送到GitHub

## 🚀 部署步骤（10分钟完成）

### Step 1: 推送代码到GitHub（3分钟）
```bash
cd /root/clawd/product_searcher
git init
git add .
git commit -m "Initial commit"
# 在GitHub.com创建空仓库
git remote add origin https://github.com/你的用户名/product-searcher.git
git push -u origin main
```

### Step 2: 部署到Render（5分钟）
1. 访问 https://dashboard.render.com
2. 用GitHub登录
3. 点击 "New +" → "Web Service"
4. 选择你的GitHub仓库
5. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. 添加环境变量：`BRAVE_API_KEY` = 你的Key
7. 点击 "Create"
8. **完成！访问给出的URL**

### Step 3: 验证部署（2分钟）
1. 打开Render给的URL
2. 测试搜索功能
3. 查看历史记录
4. 导出CSV测试

## 📖 详细指南

查看完整部署指南：`GITHUB_DEPLOY.md`

## 🎯 预期结果

部署成功后，你将获得一个公网可访问的URL，如：
- Render: `https://product-searcher.onrender.com`
- Railway: `https://product-searcher-production.up.railway.app`

## ❓ 遇到问题？

1. **部署失败？** 查看Render/Railway的Logs
2. **搜索无数据？** 检查BRAVE_API_KEY是否正确
3. **应用打不开？** 等待1-2分钟让服务启动

## 📞 获取帮助

- Render文档: https://render.com/docs
- Railway文档: https://docs.railway.app
- GitHub: 在仓库中查看Actions

---

**预计总耗时**: 10-15分钟  
**成本**: 免费
