# Render部署指南

你的代码已成功推送到GitHub：
https://github.com/xydiao/product-searcher

## 部署步骤

### 步骤1：访问Render

1. 打开浏览器访问：https://dashboard.render.com
2. 点击 "Get Started" 或 "Sign Up"
3. 选择 **"Sign up with GitHub"**
4. 用你的GitHub账号登录

### 步骤2：创建Web服务

1. 在Render Dashboard，点击 **"New +"**
2. 选择 **"Web Service"**
3. 在 "Connect a repository" 区域：
   - 找到并选择 `xydiao/product-searcher` 仓库
   - 点击 **"Connect"**

### 步骤3：配置服务

在配置页面填写以下信息：

| 配置项 | 值 |
|--------|-----|
| **Name** | `product-searcher` |
| **Root Directory** | (留空) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | `Free` (免费) |

### 步骤4：添加环境变量

在 "Environment Variables" 部分添加：

| Key | Value |
|-----|-------|
| `BRAVE_API_KEY` | `BSAgdn1sl1bYrniqvGdpRAefrqF5glX` |
| `PORT` | `10000` |

**重要**：确保两个环境变量都添加正确！

### 步骤5：创建服务

点击页面底部的 **"Create Web Service"**

### 步骤6：等待部署完成

- 首次部署需要2-5分钟
- 可以在 "Logs" 标签查看进度
- 部署成功后状态会变为 **"Live"**

---

## 访问你的应用

部署成功后，在服务页面顶部会显示访问URL，如：
```
https://product-searcher-xxxx.onrender.com
```

这个就是你的公网访问地址！🎉

---

## 测试步骤

1. 在浏览器中打开你的Render URL
2. 在搜索框输入关键词（如："AI toys"）
3. 选择平台（Amazon或TikTok）
4. 点击搜索
5. 确认能看到搜索结果
6. 访问 "历史记录" 页面
7. 确认之前的搜索记录已保存

---

## 常见问题

### Q: 部署失败怎么办？

A: 
1. 点击服务页面的 "Logs" 标签
2. 查看具体错误信息
3. 常见问题：
   - 依赖安装失败：检查requirements.txt
   - 端口配置错误：确认PORT=10000
   - API Key无效：检查BRAVE_API_KEY

### Q: 搜索没有结果？

A: 
1. 确认BRAVE_API_KEY已添加且正确
2. 检查Render服务状态是否为"Live"
3. 尝试更换关键词（如 "robot dog"）

### Q: 如何更新代码？

A: 
```bash
# 本地更新后
git add .
git commit -m "Update"
git push origin main

# Render会自动重新部署
```

### Q: 免费版有什么限制？

A: 
- 每月750小时运行时间
- 空闲时会休眠（首次访问需要30秒唤醒）
- 自动HTTPS

---

## 下一步操作

1. **现在访问**：https://dashboard.render.com
2. **用GitHub登录**
3. **按上面的步骤创建Web服务**
4. **完成后告诉我你的访问URL**

---

## 验证部署成功

部署成功后，你应该能：
✅ 在浏览器打开Render URL
✅ 看到搜索首页
✅ 搜索产品并看到结果
✅ 访问历史记录页面看到保存的搜索

---

## 需要帮助？

遇到问题随时问我！截图发给我更清楚。
