# 灵感库 linggan

个人灵感管理页面：**科学灵感 / 发明灵感 / 科普创作灵感 / 魔术灵感** 四大类的浏览、搜索、筛选与实时录入（850+ 条，来自华为备忘录导出文件的合并整理）。

## 使用

- 打开 👉 https://anosniff.github.io/linggan/
- **首次打开**：设置访问密码（所有灵感数据将自动转为 AES-256 密文存储，仓库里的明文数据文件会被自动删除）
- 之后每次打开：输入密码解锁 → 顶部面板录入新灵感 → 保存后自动加密提交回仓库

## 密码与加密说明

- 密码只保存在你的浏览器本地（localStorage），不会上传；用于校验和派生加密密钥（PBKDF2 + AES-256-GCM）
- 灵感数据存于仓库 `data.enc`，录入存于 `linggan-entries.enc`，均为密文——即使查看网页源码或仓库文件也看不到内容
- 忘记密码无法解锁（数据密文不可破解）；可联系 AI 助手用本地原始 docx 文件帮你重置
- 「🔑 修改密码」会重新加密云端数据

## 开启录入同步（GitHub 云同步）

1. GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens** → Generate new token
   - Repository access：选择本仓库 `anosniff/linggan`
   - Permissions：只勾 **Contents → Read and write**（其余全部不勾）
2. 锁屏页的「GitHub 配置」里填仓库 `anosniff/linggan`、分支 `main`、粘贴 Token → 保存；或解锁后在「☁️ GitHub 云同步」面板填写
3. 之后每次录入/删除都会自动加密提交回仓库，换设备、换浏览器、下次打开数据都还在

> ⚠️ Token 只保存在你的浏览器本地，不会出现在仓库或页面代码里；他人打开页面只能看到登录页，无法读取或写入。

## 本地 / 服务器部署

```bash
python3 server.py        # 打开 http://127.0.0.1:8080/（用本仓库的 灵感库.html，内含数据与锁屏）
```

页面自动检测三种模式：🟢 服务器自动保存 / 🟦 GitHub 云同步 / 🟡 本地模式。
