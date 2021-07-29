import os 
import argparse
import re

from dotenv import load_dotenv
load_dotenv() # secret_key 불러오기 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.prod")
import django
django.setup()


from clipper.course_save import save as course_save
from clipper.inflearn import get_courses as get_inflearn_courses
from clipper.nomad import get_courses as get_nomad_courses

if __name__ == '__main__':
    # args로 -n <사이트이름> 과 옵션 -p <page> 을 받아 분기시켜 저장을 실행한다.
    parser = argparse.ArgumentParser(description="Save study courses in a web-page.")
    parser.add_argument('-n', '--name')
    parser.add_argument('-p', '--page', dest='page', default=0)
    args = parser.parse_args()


    # 강의사이트이름이 입력되면 해당 강의정보를 저장한다.
    if re.match("인프런", args.name):
        # 인프런 데이터 저장
        inflearn_courses = get_inflearn_courses() # 인프런 스크래핑
        course_save(inflearn_courses, "인프런")
        print(args.name, "의 강의 정보를 Database에 저장합니다.")
    elif re.match("nomad", args.name):
        # 노마드코더 데이터 저장
        nomad_courses = get_nomad_courses()
        course_save(nomad_courses, "nomadcoders")

    else:
        print("-n <강의 사이트 이름>")

    # 이와 더불어 특정 page 정보를 입력한 경우.
    if args.page:
        print(args.name, "의 page=", args.page, "의 강의 정보를 Database에 저장합니다.")
