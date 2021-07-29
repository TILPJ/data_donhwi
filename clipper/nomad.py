"""
크롤링하는데 여러 번 실패해 본 결과, 
다음과 같은 크롤링 전략이 가장 효과적이었다.
1. 셀레늄 웹드라이버로 웹페이지를 얻는다.
2. 셀레늄 execute 명령으로 그 웹페이지의 <html>태그 내용물을 innerHTML로 리턴시켜
3. 만든 soup 객체를 가지고 
4. 분석한다.
https://stackoverflow.com/questions/62165635/how-to-scrape-data-from-flexbox-element-container-with-python-and-beautiful-soup
"""
import requests
from requests.compat import urljoin, quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import os

# constants
BASE_URL = "https://nomadcoders.co/"
COURSES_URL = urljoin(BASE_URL, "/courses")
CHALLENGES_URL = urljoin(BASE_URL, "/challenges")
WAIT = 2 # seconds


# chromedriver options
def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def max_window(browser):
    total_width = browser.execute_script("return document.body.offsetWidth")
    total_height = browser.execute_script("return document.body.scrollHeight")
    browser.set_window_size(total_width, total_height)

def get_soup_from_page(url, chrome_options, xpath=None):
    """
    webpage의 url과 chromedriver의 option항목들을 받아 
    webpage <html> 태그 내용물 전체를 soup 객체로 반환하는 메서드.
    xpath는 브라우저 윈도우 확장을 명하는 button 엘리먼트의 xpath 스트링값이다.

    """

    # 웹드라이버 세션을 실행하는 동안 본격적인 스크래이핑 작업을 위해
    # 웹페이지의 모든 DOM들이 들어가도록 soup 인스턴스를 생성한다.
    with webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=set_chrome_options()) as browser:
        
        browser.get(url)
        max_window(browser)
        browser.implicitly_wait(WAIT)

        # 펼칠 필요가 있는 경우 버튼을 클릭하여 브라우저를 펼친다.
        if xpath:
            try:
                button = browser.find_element_by_xpath(xpath)
                button.click()
                max_window(browser)
            except Exception:                
                xpath=None
                print("See all 버튼이 없습니다.")
        
        # <html> 태그 내용물을 얻는다.
        html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

        # soup로 만들되 가급적 'lxml' 파서를 이용한다.
        try:
            soup = BeautifulSoup(html, 'lxml')
        except Exception:
            soup = BeautifulSoup(html, 'html.parser')
        # browser 세션을 종료하고 브라우저를 닫는다.

    
    return soup


def extract_courses(cards):
    
    
    course_info = []

    counter = 1

    for card in cards:
        print(counter, end=" ")
        course = extract_course(card)
        course_info.append(course)
        counter += 1

    return course_info


def extract_course(card):

    # 캐치 못하는 경우 고려
    try:
        title = card.find("h3").get_text(strip=True)
    except Exception:
        title = "-"
    try:
        description = card.find("h4").get_text(strip=True)
    except Exception:
        description = "-"
    try:
        thumbnail_link = card.find("img")["src"]
    except Exception:
        thumbnail_link = "-"

    instructor = "니꼬샘"

    course_link = card.find("a")["href"]
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


# 각 강의의 챕터 목록 추출
def extract_chapter_list(link):
    xpath = "//button[contains(text(),'See all')]"
    chrome_options = set_chrome_options()
    soup = get_soup_from_page(link, chrome_options, xpath)
    curriculum = soup.find('div', string=re.compile("curriculum", re.I))
    chapters = curriculum.parent.find_all('span', string=re.compile("#[0-9][^.][^.]"))
    
    chapter_list = []
    for chapter in chapters:
        chapter_name = chapter.get_text()
        
        section_list = []
        for section in chapter.parent.select("button"):
            section_list.append(section.select_one("span").get_text())
        
        chapter_list.append({
                "chapter" : chapter_name,
                "section_list" : section_list
            })
        
    return chapter_list

def get_courses():
    chrome_options = set_chrome_options()
    
    # 이제 soup로 본격적인 스크래이핑 작업에 들어간다.
    soup = get_soup_from_page(COURSES_URL, chrome_options)
    # card가 담긴 태그
    cards = soup.find_all("div", class_="sc-bdfBwQ znekp flex flex-col items-center")
    courses_info = extract_courses(cards)

    return courses_info

data = get_courses()