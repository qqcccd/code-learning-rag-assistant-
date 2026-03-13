# 官方稳定Python镜像，兼容你的项目
FROM python:3.10-slim

# 基础环境配置
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# 设置容器工作目录
WORKDIR /app

# 复制项目所有文件
COPY . .

# 安装Python依赖
RUN pip install -r requirements.txt

# 暴露平台要求的端口
EXPOSE 7860

# 启动后端服务
CMD ["python", "backend/main.py"]