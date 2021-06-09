# 설치한 패키지 
- python 3.8.10
- django 3.2.3
- requests 
- beautifulsoup4
- psycopg2-binary 
- python-dotenv

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
- Section 모델 name 필드를 Textfield -> CharField로 변경 

manage.py 
- python-dotenv로 분리한 .env 파일을 불러오기 위한 로직 추가 

.env 파일 추가 
![스크린샷 2021-06-09 오후 8 57 22](https://user-images.githubusercontent.com/80886445/121350172-4c111580-c965-11eb-814e-00062ef2e1d4.png)

start.py 수정 (_레포에 스크래핑 샘플 폴더에 제가 구현해 놓았던 main.py 파일을 이름을 바꾸고 안에 로직을 추가했습니다)

inflearn_save.py 추가 (inflearn.py 파일에서 스크랩 후 최종으로 리턴된 리스트를 넘겨받아 DB에 저장하는 파일입니다)


