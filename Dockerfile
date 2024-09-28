# 베이스 이미지 설정 (Python 3.9 사용)
FROM python:3.9-slim

# 작업 디렉토리 생성
WORKDIR /app

# 필요한 파일들을 작업 디렉토리로 복사
COPY requirements.txt requirements.txt
COPY . .

# pip 최신 버전으로 업데이트 및 필요한 패키지 설치
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 웹 애플리케이션 실행 포트 설정
EXPOSE 5000

# 애플리케이션 실행 명령어
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
