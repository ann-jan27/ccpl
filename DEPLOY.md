# 快速部署指南

## 方式一：Docker 镜像部署 (推荐)

我们已经在 GitHub Container Registry (GHCR) 上发布了预构建的镜像，您可以直接拉取运行。

### 1. 准备环境
创建一个目录用于存放数据：
```bash
mkdir ccpl && cd ccpl
mkdir data
```

### 2. 创建 docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    image: ghcr.io/exekiel179/ccpl-app:latest
    container_name: ccpl-system
    ports:
      - "8080:80"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
```

### 3. 启动
```bash
docker-compose up -d
```

---

## 方式二：手动构建部署

如果您修改了代码（例如更改了管理员密码），需要重新构建镜像。

### 1. 修改代码
在 `admin.html` 中搜索 `ADMIN_PWD` 并修改为您自己的密码。

### 2. 构建镜像
```bash
docker build -t ccpl-app:custom .
```

### 3. 运行容器
```bash
docker run -d \
  -p 8080:80 \
  -v $(pwd)/data:/app/data \
  --name ccpl-custom \
  ccpl-app:custom
```

---

## 本地开发调试

如果您想在本地 Python 环境运行：

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行后端：
```bash
uvicorn main:app --reload --port 8000
```

3. 访问：
- 填写页：`http://localhost:8000/`
- 后台：`http://localhost:8000/admin`

---

## 常见问题

### 1. 数据保存在哪里？
数据保存在容器内的 `/app/data/submissions.db` 文件中。通过挂载，它会同步到您宿主机的 `./data` 目录下。

### 2. 容器删除后数据会丢失吗？
只要您配置了 `volumes` 挂载，数据就会安全地保存在宿主机硬盘上，即使删除容器再重新创建，数据也会自动恢复。

### 3. 如何备份？
直接备份宿主机 `./data/submissions.db` 文件即可。
