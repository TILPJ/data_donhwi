import requests
from bs4 import BeautifulSoup


# 인프런 > 강의 > 개발/프로그래밍
URL = "https://www.inflearn.com/courses/it-programming"


# 마지막 페이지 추출
def get_last_page():

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    pagination = soup.find("ul", {"class":"pagination-list"})
    last_page = pagination.find_all("li")[-1].string

    return int(last_page)


# 각 챕터의 섹션 목록 추출
def extract_section_list(html):

    section_list = []

    sections = html.find_all("span", {"class":"ac-accordion__unit-title"})
    for section in sections:
        section_list.append(section.string)

    return section_list


# 각 강의의 챕터 목록 추출
def extract_chapter_list(link):

    chapter_list = []

    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("div", {"class":"cd-accordion__section-cover"})

    for result in results:
        chapter_name = result.find("span", {"class":"cd-accordion__section-title"})
        if chapter_name:
            chapter_name = chapter_name.string   

        section_list = extract_section_list(result)

        chapter_list.append({
            "chapter" : chapter_name,
            "section_list" : section_list
        })

    return chapter_list


# 각 강의에서 강의 정보(강의명, 대표이미지, 설명, 강사, 강의링크) 추출
def extract_course(html):
    """
    * 주의 * 
    title = html.find("div", {"class":"course_title"}).string 으로 해줘도 되지만, title이 없는 경우가 있을 수도 있다
    title이 없는 경우에 => AttributeError: 'NoneType' object has no attribute 'string' 에러가 발생한다
    해당 오류를 방지하기 위해 아래와 같이 if문으로 한번 체크를 해준다
    description, instructor도 동일
    """
    title = html.find("div", {"class":"course_title"})
    if title:
        title = title.string

    thumbnail_link = html.find("div", {"class":"card-image"}) # 대표이미지가 video인 경우가 있다
    if thumbnail_link.find("img"):
        thumbnail_link = thumbnail_link.find("img")["src"]
    elif thumbnail_link.find("source"):
        thumbnail_link = thumbnail_link.find("source")["src"]

    description = html.find("p", {"class":"course_description"})
    if description:
        description = description.string

    instructor = html.find("div", {"class":"instructor"})
    if instructor:
        instructor = instructor.string

    course_link = html.find("a", {"class":"course_card_front"})["href"]
    course_link = f"https://www.inflearn.com{course_link}"

    chapter_list = extract_chapter_list(course_link)

    return {
        "title" : title,
        "thumbnail_link" : thumbnail_link,
        "description" : description,
        "instructor" : instructor,
        "course_link" : course_link,
        "chapter_list" : chapter_list
    }


# 존재하는 모든 페이지의 url을 만들고 request하여 각 페이지의 모든 강의를 추출
# 1페이지 url = https://www.inflearn.com/courses/it-programming?page=1
# 2페이지 url = https://www.inflearn.com/courses/it-programming?page=2
# ... 
def extract_courses(last_page):

    courses_info = []

    # for page in range(1, last_page+1):
    for page in range(1, 2): # 테스트 로직
        print(f"=====Scrapping page {page}=====")
        response = requests.get(f"{URL}?page={page}")
        soup = BeautifulSoup(response.text, "html.parser")
        # 각 페이지의 모든 강의 추출
        results = soup.find("div", {"class":"courses_card_list_body"}).find_all("div", {"class":"column"})
        
        for result in results:
            course = extract_course(result)
            courses_info.append(course)

    return courses_info


def get_courses():
    last_page = get_last_page()
    courses_info = extract_courses(last_page)

    return courses_info