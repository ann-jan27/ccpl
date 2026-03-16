FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 创建数据目录
RUN mkdir -p /app/data

# 暴露端口（FastAPI 默认可以使用 80）
EXPOSE 80

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
