import os 
from dotenv import load_dotenv
load_dotenv() # secret_key 불러오기 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

from inflearn import get_courses as get_inflearn_courses 
from inflearn_save import save as inflearn_save 


if __name__=='__main__':
    
    inflearn_courses = get_inflearn_courses() # 인프런 스크래핑 
    inflearn_save(inflearn_courses) # 인프런 데이터 저장

    # print(inflearn_courses)

