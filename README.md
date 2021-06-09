# 설치되 패키지 
python 3.8.10
django 3.2.3
requests 
beautifulsoup4
psycopg2-binary 
python-dotenv

# 환경 
python-dotenv로 환경변수를 분리해서 관리(secret_key, database 정보)

# (6/9) 수정한 부분
conf > settings.py 
- import os 추가
- secret key
- installed_apps 부분을 django_apps와 project_apps로 구분함 
- time_zone을 Asia/Seoul로 변경 
- 그 외 동일 

clipper > admin.py
- models를 admin 사이트에 등록 

clipper > models.py
- Site 모델 추가 
- Course 모델에 site foreign 필드 추가 
- Chapter, Section 모델에서 content -> name으로 필드명 변경


