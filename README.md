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

---
# 변경 사항(느릿느릿 2021-06-16)
- 유데미의 thumbnail link는 길이가 디폴트값 200을 넘는게 많다. **urlfield의 max_length=500 으로 변경**하고 makemigrations, migrate.  
- 유데미는 영어강의도 수집했다. (페이지10 이하로만)
- 유데미 개발 카테고리 이외에 IT, 디자인, 음악 등 컴퓨터 프로그램 관련 강의를 중심으로 추가해 봤다.
- get_soup_from_page 메서드에 화면 스크롤 액션을 추가함.(유데미 강의 목록의 썸네일 이미지 링크를 온전히 페이지에 렌더링시키기 위함.)
- 한 페이지당 크롤링 소요 시간은 WAIT * 2 이상이며 한 강의당 1.0625 페이지이므로 강의 1000개를 한 번에 스크래이핑 하는데 소요되는 시간은 최소 WAIT*2125 = 10625초 = 177분 = 3시간 이다.
- 병렬 스크래이핑 구현을 고민해봐야 할듯.
---
# References
- Xpath cheatsheet : https://devhints.io/xpath#indexing
- 장고 모델 URLField : https://docs.djangoproject.com/en/3.2/ref/models/fields/
