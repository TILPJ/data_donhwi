import requests
from requests.compat import urljoin, quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re

### constants ###

BASE_URL = "https://www.udemy.com"

##대상 카테고리
# a. 개발
# b. IT 및 소프트웨어
# c. 디자인
# d. 음악 - 음악 소프트웨어
CATEGORIES = {
    "개발": "/ko/courses/development",
    # "IT 및 소프트웨어": "/ko/courses/it-and-software",
    # "디자인": "/ko/courses/design",
    # "음악 소프트웨어": "/ko/courses/music/music-software"    
}

## 검색조건식 적용 순서
# 1. 한국어 + 가장 인기 있는
# 2. 영어 + 가장 인기 있는 + 평가>4.5
KEYS = [
    ("?lang=ko", "&sort=popularity"),
    # ("?lang=en", "&rating=4.5&sort=popularity")
    ]

WAIT = 5 # seconds


# chromedriver options
def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def max_window(browser):
    total_width = browser.execute_script("return document.body.offsetWidth")
    total_height = browser.execute_script("return document.body.scrollHeight")
    browser.set_window_size(total_width, total_height)

def get_soup_from_page(url, chrome_options, target_xpath='/html', button_xpath=None):
    """
    webpage의 url과 chromedriver의 option항목들을 받아 
    webpage <html> 태그 내용물 전체를 soup 객체로 반환하는 메서드.
    target_xpath는 수집하려는 정보가 담긴 minimal 엘리먼트의 xpath.
    (예: 페이지 전체를 soup에 담으려면 '/html'. 그러나 깊히 안잡히는 경우가
    있을 수 있으므로 가급적 범위를 좁혀 정한다.)
    브라우저를 천천히 scrolldown하여 숨겨진 엘리먼트들이 화면에 뜨도록 한다.
    button_xpath는 브라우저 윈도우 확장을 명하는 button 엘리먼트의 xpath 스트링값이다.

    """

    # 웹드라이버 세션을 실행하는 동안 본격적인 스크래이핑 작업을 위해
    # 웹페이지의 모든 DOM들이 들어가도록 soup 인스턴스를 생성한다.
    with webdriver.Chrome(options=chrome_options) as browser:
        
        browser.implicitly_wait(WAIT)        
        browser.get(url)
        max_window(browser)

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(WAIT)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        # 펼칠 필요가 있는 경우 버튼을 클릭하여 브라우저를 펼친다.
        if button_xpath:
            try:
                button = browser.find_element_by_xpath(button_xpath)
                button.click()                
            except Exception:                
                print(".", end="")
        max_window(browser)
        browser.save_screenshot("courses.png")
        # 타겟엘리먼트가 있으면 엘리먼트의 innerHTML 정보를 수집한다.
        blank = False
        try:
            element = browser.find_element_by_xpath(target_xpath)            
        except Exception:
            blank = True
        
        if not blank:            
            html = element.get_attribute("innerHTML")
        
        
        # soup로 만들되 가급적 'lxml' 파서를 이용한다.
            try:
                soup = BeautifulSoup(html, 'lxml')
            except Exception:
                soup = BeautifulSoup(html, 'html.parser')
        else:
            print('Page:Blank')
            soup = None
            
        # browser 세션을 종료하고 브라우저를 닫는다.    
    return soup



def extract_course(card):

    # 캐치 못하는 경우 고려
    try:
        title = card.find("div", class_=re.compile("title")).get_text(strip=True)
    except Exception:
        title = "-"
    try:
        description = card.find('p', class_=re.compile("course-headline")).get_text(strip=True)
    except Exception:
        description = "-"
    try:
        thumbnail_link = card.find("img")["src"]
    except Exception:
        thumbnail_link = "-"
    try:
        instructor = card.find('div', class_=re.compile("instructor")).get_text(strip=True)
    except Exception:
        instructor = "-"

    course_link = card["href"]
    course_link = urljoin(BASE_URL, course_link)

    chapter_list = extract_chapter_list(course_link)

    return {
        "title" : title,
        "thumbnail_link" : thumbnail_link,
        "description" : description,
        "instructor" : instructor,
        "course_link" : course_link,
        "chapter_list" : chapter_list
    }


def extract_courses(cards):
    """
    한 페이지에서 추출할 수 있는 강의들 정보를 리스트형태로 반환한다,
    """
    courses_info = []

    for card in cards:
        courses_info.append(extract_course(card))
        print(",", end="")
        
    return  courses_info

def extract_chapter_list(link):
    # 옵션설정 및 리턴값 초기화
    chrome_options = set_chrome_options()
    chapter_list = []
    
    target_xpath = '//div[@data-purpose="course-curriculum"]'
    button_xpath = '//button[@data-purpose="expand-toggle"]'
    soup = get_soup_from_page(link, chrome_options, target_xpath, button_xpath)
    
    chapters = soup.find_all("div", class_=re.compile("section--panel"))
    for chapter in chapters:
        section_list = []
        for section in chapter.find_all("li"):
            section_list.append(section.get_text(strip=True))
        title = chapter.find("span", class_=re.compile("title")).get_text(strip=True)
        chapter_list.append({
                    "chapter": title,
                    "section_list": section_list
                    })
        
    return chapter_list


def get_courses():
    
    # 옵션설정 및 리턴값 초기화
    chrome_options = set_chrome_options()
    courses_info = [] 
    
    # 스크래이핑 시작 페이지 url 결정하기      
    for _, cat in CATEGORIES.items():
        category_url = urljoin(BASE_URL, cat)
        for key in KEYS: 
            # 페이지 번호, 최대 페이지번호, 강의 갯수를 초기화한다.
            page = 0
            max_page = 1
            number_of_courses = 0
            # 페이지 번호가 10 이하에 올려진 강의들만 추출한다.
            # max_page 최소값을 조정해야 한다.
            while page >= 0 and page <= min(max_page, 10):                
                if page:
                    url = urljoin(category_url, key[0] + f"&p={page}" + key[1])
                else:
                    url = urljoin(category_url, "".join(key))
                    print("")
                    print(f"==={url}===")

                
                # 이제 soup로 본격적인 스크래이핑 작업에 들어간다.
                # 원하는 정보가 모두 담긴 최소외각의 xpath는 다음과 같다.
                target_xpath = '//div[contains(@class,"course-directory--container")]'            
                soup = get_soup_from_page(url, chrome_options, target_xpath)

                # 먼저 강의 수에 따라 페이지가 나뉠 수 있으므로 처음 한 번만 체크하고 기록한다.
                if page == 0:
                    page += 1   
                    try:
                        number_of_courses = soup.find('span', string=re.compile("개의 결과"))
                        number_of_courses = int(re.findall("\d+", number_of_courses.get_text())[0])
                    except Exception:
                        number_of_courses = 0


                print(page, end="page: ")

                if number_of_courses > 16:
                    max_page =  number_of_courses // 16 + 1
                # 강의수가 16 개 초과이면 max_page >= 2 이므로 루프를 돈다.     
                page += 1
                cards = soup.select('a["id"]')
                courses_info += extract_courses(cards)    

    return courses_info 

