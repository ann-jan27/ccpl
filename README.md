# ccplccpl信息收集系统

[![GitHub Release](https://img.shields.io/github/v/release/Exekiel179/ccpl)](https://github.com/Exekiel179/ccpl/releases)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://ghcr.io/exekiel179/ccpl-app)

一个轻量级的全栈信息收集与管理系统，基于 FastAPI 和 SQLite 构建，支持成员信息实时汇总与导出。

## 功能特性

- 📝 **实时汇总** - 成员提交信息后，管理员可在后台立即查看，无需手动同步
- 📊 **后台管理** - 密码保护的管理界面，支持实时查看、单条删除、清空或导出 CSV
- 🖼️ **证件照上传** - 支持 JPG/PNG 格式，自动转为 Base64 存储
- 📅 **动态年份** - 入学年份自动生成，支持 2026 及未来年份
- 💾 **持久化存储** - 使用 SQLite 数据库存储在服务器本地，支持 Docker 数据卷挂载
- 📱 **响应式设计** - 完美适配桌面和移动设备端

## 快速开始

### 方式一：使用 Docker Compose (推荐)

这是最简单的部署方式，会自动处理所有配置：

1. 克隆仓库：
```bash
git clone https://github.com/Exekiel179/ccpl.git
cd ccpl
```

2. 准备环境文件：
```bash
cp .env.example .env
```

3. 启动服务：
```bash
docker-compose up -d
```

4. 访问系统：
   - **填写页**：`http://localhost:8080/`
   - **管理后台**：`http://localhost:8080/admin` (默认密码：`lab2024`)

### 方式二：直接拉取镜像运行

```bash
docker run -d \
  -p 8080:80 \
  -v $(pwd)/data:/app/data \
  --name ccpl-app \
  ghcr.io/exekiel179/ccpl-app:latest
```

## 目录结构

```
.
├── main.py            # FastAPI 后端程序
├── form.html          # 信息收集前端页面
├── admin.html         # 管理后台前端页面
├── Dockerfile         # 镜像构建脚本
├── docker-compose.yml # 容器编排配置
├── requirements.txt   # Python 依赖列表
└── data/              # 数据库目录 (自动创建)
```

## 技术栈

- **后端**: Python 3.11, FastAPI, Uvicorn
- **数据库**: SQLite (本地文件存储)
- **前端**: Vanilla JS, HTML5, CSS3 (无外部依赖)
- **部署**: Docker, GitHub Actions

## 注意事项

1. **数据安全**：请务必挂载 `/app/data` 目录到宿主机，否则容器删除后数据会丢失。
2. **管理员密码**：默认密码为 `lab2024`。如需修改，请编辑 `admin.html` 中的 `ADMIN_PWD` 常量并重新构建镜像。
3. **备份**：建议定期备份宿主机上的 `./data/submissions.db` 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

## License

MIT License
