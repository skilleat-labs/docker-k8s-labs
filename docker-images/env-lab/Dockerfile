# ✅ 개선 버전: ENV는 기본값만, 실제 값은 실행 시 주입
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

# 기본값만 설정 — 실행 시 -e 또는 env_file로 덮어씀
ENV APP_ENV=development
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_PASSWORD=

EXPOSE 5000
CMD ["python", "app.py"]
