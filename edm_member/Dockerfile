# Python 이미지 사용
FROM python:3.11.5

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# 프로젝트 파일 복사
COPY . .

# collectstatic 명령 실행
RUN python manage.py collectstatic

# Gunicorn 실행
CMD ["gunicorn", "-b", "0.0.0.0:8000", "edm_user.wsgi:application"]