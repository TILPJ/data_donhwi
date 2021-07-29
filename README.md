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
- secret key 부분 수정 
- installed_apps 부분을 django_apps와 project_apps로 구분함 
- time_zone을 Asia/Seoul로 변경 
- 그 외 동일 

clipper > admin.py
- models를 admin 사이트에 등록 

clipper > models.py
- Site 모델 추가 (site 테이블의 데이터는 admin 페이지에서 밀어넣었습니다)
- Course 모델에 site foreign 필드 추가 
- Chapter, Section 모델에서 content -> name으로 필드명 변경
- Section 모델 name 필드를 Textfield -> CharField로 변경 

manage.py 
- python-dotenv로 분리한 .env 파일을 불러오기 위한 로직 추가 

.env 파일 추가 (secret key와 db 정보가 들어있습니다)

![스크린샷 2021-06-09 오후 8 57 22](https://user-images.githubusercontent.com/80886445/121350172-4c111580-c965-11eb-814e-00062ef2e1d4.png)

start.py 파일 수정 
- '_' 레포에 스크래핑 샘플 폴더에 제가 구현해 놓았던 main.py 파일을 이름을 바꾸고 안에 로직을 추가했습니다)

inflearn_save.py 파일 추가 
- inflearn.py 파일에서 스크랩 후 최종으로 리턴된 리스트를 넘겨받아 DB에 저장하는 파일입니다)
- inflean.py 파일에 db에 저장하는 로직까지 넣기에는 몸집이 커질것 같아 파일을 분리했습니다 

inflearn.py 파일은 수정하지 않았습니당

# 실행 방법
start.py 파일을 실행하거나, 터미널에서 python start.py 를 입력하여 실행합니다 


---
# 변경 사항(느릿느릿 2021-06-13)
- start.py -> start_clipper.py   
cli 명령 예시:
```linux
>> python start_clipper.py -n 인프런
```
- inflearn_save.py -> clipper/inflearn_save.py   
> Course 중복 저장 방지
> Constructor 이용한 DB 저장코드 통일(https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_one/)

- inflearn.py -> clipper/inflearn.py   
> requests.compat.urljoin 추가함.(url manipulator)
> URL 분리   
tested at 2021-06-13 and found some errors like
```
psycopg2.errors.StringDataRightTruncation: value too long for type character varying(200)
DataError: value too long for type character varying(200)
```
---

# 변경 사항(느릿느릿 2021-06-14)
- inflearn_save.py -> course_save.py 로 공용 세이버로 만듦
- nomadcoders courses 카테고리 저장 확인 `python start_clipper.py -n nomad`

# 변경 사항(donhwi 2021-07-22)
- clipper>models.py 
- "django.db.utils.DataError: value too long for type character varying(200)" 오류가 발생하여 전체적으로 max_length의 길이를 늘렸습니다

# 변경 사항(donhwi 2021-07-29)
1. 서버/개발환경을 위한 settings 분리
- 이전 : conf>settings.py 
- 이후 : conf>settings>base.py, local.py, prod.py
- settings 환경 분리에 따른 개발 환경에서의 서버 실행 방법 : python manage.py runserver --settings=conf.settings.local

2. .env 데이터베이스 관련 환경 변수명 수정, conf.settings.local.py 파일에서 DATABASES 설정 부분 환경 변수명 변경됨
- 이전 : DATABASE_ENGINE, DATABASE_NAME 등
- 이후 : LOCAL_DATABASE_ENGINE, LOCAL_DATABASE_NAME 등
