from clipper.models import Site, Course, Chapter, Section

# 섹션 정보 저장
def section_info_save(chapter_id, section_list):

    for section in section_list:
        data = Section(name=section,
                        chapter_id=chapter_id
                        )
        data.save()


# 챕터 정보 저장
def chapter_info_save(course_id, chapter_list):
    
    for chapter in chapter_list:
        data = Chapter(name=chapter["chapter"],
                        course_id=course_id
                        )
        data.save()
        
        section_list = chapter["section_list"]
        section_info_save(data.id, section_list)


# 강의 정보 저장 
def course_info_save(courses):
    site_id = Site.objects.get(name__contains='인프런').id

    for course in courses:
        # data unpacking
        data = Course(title=course["title"], 
                        thumbnail_link=course["thumbnail_link"], 
                        description=course["description"], 
                        instructor=course["instructor"], 
                        course_link=course["course_link"], 
                        site_id=site_id
                        )
        data.save()
        
        chapter_list = course["chapter_list"]
        chapter_info_save(data.id, chapter_list)

    
# inflean.py 파일에서 스크랩하여 저장한 리스트를 받아서 데이터베이스에 저장
def save(courses):
    course_info_save(courses)