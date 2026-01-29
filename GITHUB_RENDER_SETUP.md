# GitHub + Render 部署完整指南

## 第一步：创建GitHub仓库

### 1.1 在GitHub.com创建仓库

1. 访问 https://github.com
2. 登录你的账号（邮箱：21291742@qq.com）
3. 点击右上角 "+" → "New repository"
4. 填写：
   - **Repository name**: `product-searcher`
   - **Description**: 产品搜索爬虫应用 - 支持亚马逊、TikTok多平台
   - **Public/Private**: 选择 Public（免费）
   - **不要勾选** "Add a README file"
5. 点击 "Create repository"

### 1.2 创建访问令牌（Personal Access Token）

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 配置：
   - **Note**: `product-searcher-deploy`
   - **Expiration**: 选择 "90 days"
   - **Select scopes**: 勾选 ✅ `repo` (完全控制私有仓库)
4. 点击页面底部的 "Generate token"
5. **重要**：复制生成的token（格式：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

⚠️ **安全提醒**：
- Token只显示一次，请立即保存到安全的地方
- 不要分享给他人
- 90天后需要重新创建

---

## 第二步：推送代码到GitHub

### 方法A：使用命令行（推荐）

在你的电脑上（不是服务器）打开终端：

```bash
# 1. 克隆空仓库
git clone https://github.com/你的用户名/product-searcher.git

# 2. 进入目录
cd product-searcher

# 3. 从服务器复制代码
# 从服务器下载：/root/clawd/product_searcher/ 目录下的所有文件
# 或者让我告诉你如何传输文件

# 4. 推送代码
git add .
git commit -m "Initial commit: 产品搜索爬虫应用"
git push origin main
```

### 方法B：使用GitHub Desktop（更简单）

1. 下载安装 GitHub Desktop：https://desktop.github.com
2. 登录你的GitHub账号
3. 点击 "File" → "Clone Repository"
4. 选择你的 `product-searcher` 仓库
5. 将 `/root/clawd/product_searcher/` 目录下的所有文件复制到本地仓库目录
6. 在GitHub Desktop中：
   - 看到变更后，点击 "Commit to main"
   - 点击 "Push origin"

---

## 第三步：部署到Render

### 3.1 创建Render账号

1. 访问 https://dashboard.render.com
2. 点击 "Get Started" 或 "Sign Up"
3. 选择 "Sign up with GitHub"（用GitHub账号登录）
4. 授权Render访问你的GitHub

### 3.2 创建Web服务

1. 在Render Dashboard，点击 "New +"
2. 选择 "Web Service"
3. 在 "Connect a repository" 部分：
   - 选择你的 `product-searcher` 仓库
   - 点击 "Connect"

### 3.3 配置服务

在配置页面填写：

| 配置项 | 值 |
|--------|-----|
| **Name** | `product-searcher` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | `Free` |

### 3.4 添加环境变量

在 "Environment Variables" 部分添加：

| Key | Value |
|-----|-------|
| `BRAVE_API_KEY` | `BSAgdn1sl1bYrniqvGdpRAefrqF5glX` |
| `PORT` | `10000` |

### 3.5 创建服务

点击页面底部的 "Create Web Service"

---

## 第四步：访问你的应用

### 等待部署完成

- 首次部署需要2-5分钟
- 在 "Logs" 标签页查看部署进度
- 部署成功后状态会变为 "Live"

### 获取访问URL

在服务页面顶部，你会看到类似：
```
https://product-searcher-xxxx.onrender.com
```

这就是你的公网访问地址！

---

## 第五步：测试应用

1. 在浏览器中打开你的Render URL
2. 尝试搜索一个产品（如 "AI robot toys"）
3. 选择平台（Amazon或TikTok）
4. 点击搜索
5. 查看结果
6. 访问 "历史记录" 页面确认数据已保存

---

## 常见问题解决

### 问题1：Push失败，提示权限错误

**原因**：访问令牌未正确配置

**解决**：
```bash
# 更新remote URL（使用你的token）
git remote set-url origin https://ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/你的用户名/product-searcher.git

# 再次push
git push -u origin main
```

### 问题2：Render部署失败

**解决**：
1. 在Render Dashboard，点击你的服务
2. 点击 "Logs" 标签
3. 查看错误信息
4. 常见问题：
   - `pip install failed`: 检查requirements.txt
   - `module not found`: 确认依赖安装正确

### 问题3：搜索无结果

**原因**：BRAVE_API_KEY未配置或无效

**解决**：
1. 在Render Dashboard，点击你的服务
2. 点击 "Environment"
3. 检查 `BRAVE_API_KEY` 是否正确
4. 如需更换，点击编辑并保存

---

## 文件传输方式

由于服务器无法直接push到GitHub，你需要手动传输文件：

### 方式1：下载后上传

1. 在服务器上打包：
   ```bash
   cd /root/clawd
   zip -r product-searcher.zip product_searcher/
   ```
2. 下载 `product-searcher.zip` 到本地
3. 解压到GitHub仓库目录
4. 用GitHub Desktop或git push推送

### 方式2：使用SFTP

如果你的本地电脑有SFTP客户端：
1. 连接服务器：sftp root@你的服务器IP
2. 下载 `/root/clawd/product_searcher/` 目录
3. 上传到GitHub

### 方式3：复制粘贴

如果文件不多，可以：
1. 在GitHub创建仓库后，创建文件
2. 复制服务器上的代码内容
3. 在GitHub网页上创建文件并粘贴

---

## 快速检查清单

部署前确认：
- [ ] GitHub仓库已创建
- [ ] Personal Access Token已创建并保存
- [ ] 本地有代码副本（或知道如何获取）
- [ ] Render账号已关联GitHub

部署后确认：
- [ ] Render服务状态为 "Live"
- [ ] 访问URL可以打开
- [ ] 搜索功能正常
- [ ] 历史记录保存成功

---

## 下一步操作

1. **立即行动**：创建GitHub访问令牌（最重要的一步）
2. **告诉我你的GitHub用户名**
3. **我会帮你检查代码并指导推送**
4. **完成后在Render部署**

---

## 需要我帮助？

如果遇到问题：
1. 告诉我具体的错误信息
2. 截图发给我
3. 我会帮你解决

祝部署顺利！🚀
