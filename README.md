# 灵感库 linggan

个人灵感管理页面：**科学灵感 / 发明灵感 / 科普创作灵感 / 魔术灵感** 四大类的浏览、搜索、筛选与实时录入（850+ 条，来自华为备忘录导出文件的合并整理）。

## 使用

- 直接打开 👉 https://anosniff.github.io/linggan/
- 顶部面板录入新灵感：选大类 → 选/自定义标签 → 写内容 → 保存入库

## 开启录入同步（GitHub 云同步）

1. GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens** → Generate new token
   - Repository access：选择本仓库 `anosniff/linggan`
   - Permissions：只勾 **Contents → Read and write**（其余全部不勾）
   - 设置有效期后生成
2. 打开页面 → 点开「☁️ GitHub 云同步」→ 仓库填 `anosniff/linggan`、分支 `main`、粘贴 Token → **保存并连接**
3. 之后每次录入/删除都会自动提交回仓库的 `linggan-entries.json`，换设备、换浏览器、下次打开数据都还在

> ⚠️ Token 只保存在你的浏览器本地（localStorage），不会出现在仓库或页面代码里；他人打开页面只能浏览、无法写入。
> ⚠️ 仓库为公开状态，录入的内容公开可见；如需私密保存，可用 `server.py` 部署到自己的服务器。

## 本地 / 服务器部署

```bash
python3 server.py        # 打开 http://127.0.0.1:8080/，录入自动保存到本机 linggan-entries.json
```

页面会自动检测三种模式并显示徽标：🟢 服务器自动保存 / 🟦 GitHub 云同步 / 🟡 本地模式。
