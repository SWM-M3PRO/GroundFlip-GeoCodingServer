# 1. 빌드 단계: 필요한 패키지 설치 및 빌드
FROM python:3.9-slim AS builder

# 2. 시스템 의존성 설치 (빌드 도구 및 GDAL)
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. Python 패키지 의존성 파일 복사
COPY requirements.txt .

# 5. Python 패키지 설치
RUN pip install --no-cache-dir --prefix="/install" -r requirements.txt

# 6. 런타임 단계: 경량 이미지에서 애플리케이션 실행
FROM python:3.9-slim

# 7. GDAL 라이브러리 복사
RUN apt-get update && apt-get install -y \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# 8. 작업 디렉토리 설정
WORKDIR /app

# 9. 빌드된 패키지 복사
COPY --from=builder /install /usr/local

# 10. 애플리케이션 파일 및 데이터 복사
COPY . .

# 11. Flask 애플리케이션 실행을 위한 환경 변수 설정
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

# 12. GDAL 라이브러리 경로 설정
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# 13. Flask 서버 실행
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:3030", "server:app"]
# 또는 gunicorn을 사용하는 경우
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3030", "server:app"]
