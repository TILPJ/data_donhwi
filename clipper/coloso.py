import requests
from requests.compat import urljoin, quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import pprint

### constants ###

BASE_URL = "https://coloso.co.kr/"
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
    chrome_options.add_argument("--start-maximized")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def max_window(browser):
    total_width = browser.execute_script("return document.body.offsetWidth")
    total_height = browser.execute_script("return document.body.scrollHeight")
    browser.set_window_size(max(total_width, 1920), total_height)

def get_soup_from_page(url, chrome_options, target_xpath='/html', button_xpath=None, mouse_xpath=None):
    """
    webpage의 url과 chromedriver의 option항목들을 받아 
    webpage <html> 태그 내용물 전체를 soup 객체로 반환하는 메서드.
    target_xpath는 수집하려는 정보가 담긴 minimal 엘리먼트의 xpath.
    (예: 페이지 전체를 soup에 담으려면 '/html'. 그러나 깊히 안잡히는 경우가
    있을 수 있으므로 가급적 범위를 좁혀 정한다.)
    브라우저를 천천히 scrolldown하여 숨겨진 엘리먼트들이 화면에 뜨도록 한다.
    button_xpath는 브라우저 윈도우 확장을 명하는 button 엘리먼트의 xpath 스트링값이다.
    예외 캐치 인디케이터는 "." 이다.
    mouse_xpath는 마우스를 올려놓으면 펼쳐지는 엘리먼트의 xpath 스트링이다.
    예외 캐치 인디케이터는 "~" 이다.

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
        
        # 마우스를 올려놓아야 펼쳐지는 엘리먼트가 있을 경우
        if mouse_xpath:
            try:
                a = ActionChains(browser)
                m= browser.find_element_by_xpath(mouse_xpath)
                a.move_to_element(m).perform()
            except Exception:
                print("~", end="")
                
#         browser.save_screenshot("courses.png")
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

def extract_courses(cat_url):
    """
    coloso 사이트에는 두 가지 경우의 강의목록 표시방법이 사용된다. 그래서
    target_xpath도 두 가지를 준비한다.
    """
    chrome_options = set_chrome_options()
    
    # "모든 클래스"라는 text가 들어있는 아무 엘리먼트를 자손엘리먼트로 가지는 section 엘리먼트
    # //section[.//*[contains(text(), "모든 클래스")]]
    # 의 형제들 중 두 번째 section 엘리먼트
    # /following-sibling::section[2]
    target_xpath = '//section[.//*[contains(text(), "모든 클래스")]]/following-sibling::section[2]' \
         '| //*[contains(@class, "catalog-title")]/following-sibling::ul'
    soup = get_soup_from_page(cat_url, chrome_options, target_xpath=target_xpath)
    
    
    courses_info = []
    for card in soup.find_all('li', class_=re.compile("[^info]")):
        course = extract_course(card)        
        print(".", end="")
        courses_info.append(course)
    
    return courses_info

def extract_course(card):
    try:
        title = card.find(class_=re.compile("title")).get_text(strip=True)
    except Exception:
        title = "-"
    try:
        thumbnail_link = card.find("img")["src"]
    except Exception:
        thumbnail_link = "-"
    try:
        instructor = card.find_all(string=re.compile("."))[-1]
    except Exception:
        instructor = "-"
        
    course_link = card.find('a')["href"]
    course_link = urljoin(BASE_URL, course_link)
    print(course_link)
    description, chapter_list = extract_details(course_link)    

    return {'title': title,
            'thumbnail_link': thumbnail_link,
            'description': description,
            'instructor': str(instructor).strip(),
            'course_link': course_link,
            'chapter_list': chapter_list
            }

def extract_details(link):
    chrome_options = set_chrome_options()
    soup = get_soup_from_page(link, chrome_options)
    try:
        description = soup.find('div', class_="fc-card__text").get_text(strip=True)
    except Exception:
        description = "-"
    
    chapter_list = []
    for chapter in soup.select('ol'):
        try:
            chapter_title = chapter.parent.p.get_text(strip=True)
        except Exception:
            chapter_title = "-"
        
        section_list = []
        for section in chapter.find_all('li'):
            try:
                section_title = section.get_text(strip=True)
            except Exception:
                section_title = "-"
            section_list.append(section_title)
        
        chapter_list.append({
            'chapter': chapter_title,
            'section_list': section_list                 
            })
            
    if not chapter_list:
        try:
            parts = soup.find_all(string=re.compile("^PART"))
            sections = soup.find_all('ul', class_='container__cards')
        except Exception as e:
            print(e)
            
        for part, section in zip(parts, sections):
            section_list = section.find_all(string=re.compile("^SECTION"))
            chapter_list.append({
                'chapter': str(part).strip(),
                'section_list': section_list
                })
    
    return description, chapter_list

# 먼저 카테고리를 추출한다.
def get_categories(soup):
    href_list = []
    for ele in soup:
        href_list.append(urljoin(BASE_URL, ele['href']))
    return href_list

def get_courses():
    # 옵션설정 및 리턴값 초기화
    chrome_options = set_chrome_options()
    courses_info = []

    # 마우스 오버로 활성화되는 카테고리 리스트 xpath
    mouse_xpath = '//*[@id="nav-menu-1"]'
    soup = get_soup_from_page(BASE_URL, chrome_options, mouse_xpath=mouse_xpath)
    category_links = soup.find('header').find_all('div', class_='nav-menu__block')[1].find_all('a')
    category_links = get_categories(category_links)

    for category in category_links[8:]: # 임시로 제한함.
        print("")
        print(category)
        courses = extract_courses(category)
        courses_info += courses
    return courses_info