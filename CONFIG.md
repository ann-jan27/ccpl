# 配置指南

## 端口配置

### 方式 1：使用环境变量 (推荐)

项目支持通过 `.env` 文件或环境变量自定义宿主机端口。

1. 编辑 `.env` 文件：
```env
PORT=8080  # 修改为您想要的宿主机端口
```

2. 重新启动服务：
```bash
docker-compose up -d
```

### 方式 2：Docker Run 指定

```bash
docker run -d -p 3000:80 ghcr.io/exekiel179/ccpl-app:latest
```

---

## 管理员密码配置

目前管理员密码在前端 `admin.html` 中定义。

### 修改步骤：
1. 打开 `admin.html` 文件。
2. 找到第 125 行左右的：
   ```javascript
   const ADMIN_PWD = 'lab2024'; // 修改为您自己的密码
   ```
3. 重新构建 Docker 镜像或直接在宿主机修改挂载的文件。

---

## 数据库与持久化

本系统使用 **SQLite** 数据库，所有成员提交的信息都存储在容器内的 `/app/data/submissions.db`。

### 关键挂载：
在 `docker-compose.yml` 中：
```yaml
volumes:
  - ./data:/app/data
```
这确保了数据库文件保存在宿主机的 `./data` 目录下。**严禁删除此挂载，否则容器更新时数据会全部丢失。**

---

## 证件照限制

- **格式**：支持 `.jpg`, `.jpeg`, `.png`。
- **大小**：前端限制最大 5MB。
- **存储**：照片以 Base64 字符串形式直接存储在 SQLite 数据库中。

---

## 入学年份配置

系统会自动生成年份选项，逻辑如下：
- **上限**：当前年份 + 2 (例如 2026 年访问，最高可选 2028)。
- **下限**：2015 年。

如需调整，请修改 `form.html` 中的 `for` 循环逻辑。

---

## API 接口说明 (供开发者参考)

- `POST /api/submit`: 提交新成员信息。
- `GET /api/submissions`: 获取所有成员信息列表。
- `DELETE /api/submissions/{id}`: 删除指定 ID 的记录。
- `POST /api/clear`: 清空所有记录。
