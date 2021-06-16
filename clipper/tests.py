from django.test import TestCase

# Create your tests here.
from .models import Site, Course, Chapter, Section
from .course_save import course_info_save

site = Site.objects.get(name__contains='udemy')
# data = [{'title': 'C# 기초부터 윈도우 프로그램까지',
#  'thumbnail_link': 'https://img-c.udemycdn.com/',
#  'description': 'C# 2017 비주얼 프로그래밍을 능숙하게 활용하기!',
#  'instructor': 'ITGO 아이티고',
#  'course_link': 'https://www.udemy.com/course/hdc-uxmg/',
#  'chapter_list': [{'chapter': 'C# 기초부터 윈도우 프로그램까지 Part.120 lectures•7hr 48min',
#    'section': ['VS 2017 설치, Hello C# 프로그램 작성 -1Preview24:32',
#     'VS 2017 설치, Hello C# 프로그램 작성 -226:45',
#     'VS 2017 설치, Hello C# 프로그램 작성 -313:01',
#     '변수, 자료형, 값형식과 참조형식, 주석문, 형변환, 열거식, 기타형식 -123:02',
#     '변수, 자료형, 값형식과 참조형식, 주석문, 형변환, 열거식, 기타형식 -221:22',
#     '변수, 자료형, 값형식과 참조형식, 주석문, 형변환, 열거식, 기타형식 -331:36',
#     '변수, 자료형, 값형식과 참조형식, 주석문, 형변환, 열거식, 기타형식 -423:59',
#     '연산자, 연산자 우선순위 -122:30',
#     '연산자, 연산자 우선순위 -220:48',
#     '연산자, 연산자 우선순위 -325:24',
#     '연산자, 연산자 우선순위 -425:47',
#     '조건문, 반복문 -119:23',
#     '조건문, 반복문 -223:19',
#     '조건문, 반복문 -327:09',
#     '메서드, 매개변수 전달 방식 -115:26',
#     '메서드, 매개변수 전달 방식 -221:17',
#     '메서드, 매개변수 전달 방식 -326:31',
#     'OOP, 클래스, 생성자, 소멸자, 상속, 오버라이딩, 복사 -123:48',
#     'OOP, 클래스, 생성자, 소멸자, 상속, 오버라이딩, 복사 -225:50',
#     'OOP, 클래스, 생성자, 소멸자, 상속, 오버라이딩, 복사 -327:00']},
#   {'chapter': 'C# 기초부터 윈도우 프로그램까지 Part.217 lectures•6hr 43min',
#    'section_list': ['접근제한자, 구조체, 인터페이스, 추상클래스 -1Preview31:01',
#     '접근제한자, 구조체, 인터페이스, 추상클래스 -219:12',
#     '접근제한자, 구조체, 인터페이스, 추상클래스 -323:06',
#     '프로퍼티, 배열, 컬렉션 -126:50',
#     '프로퍼티, 배열, 컬렉션 -231:24',
#     '프로퍼티, 배열, 컬렉션 -323:14',
#     '프로퍼티, 배열, 컬렉션 -423:53',
#     '프로퍼티, 배열, 컬렉션 -514:20',
#     '인덱서, out24:35',
#     '제네릭 프로그래밍 -119:55',
#     '제네릭 프로그래밍 -226:30',
#     '예외처리 -121:57',
#     '예외처리 -219:35',
#     'GUI 프로그래밍 -119:28',
#     'GUI 프로그래밍 -224:32',
#     'GUI 프로그래밍 -321:52',
#     'GUI 프로그래밍 -431:22']}]}]
data = [{'title': 'C# 기초부터 윈도우 프로그램까지',
 'thumbnail_link': 'https://img-c.udemycdn.com/course/240x135/1425460_f495_2.jpg?Expires=1623892048&Signature=K9gCGiwopokT~qVKfhLcAP9kL9WQZD9eI88bwhtougEk48Ht1bpYZbIoEoRIX0X-6BWpe-Jf10k1JkEO2~r8goYKt0lhegFzWneC9zLZg8RrFpbTx7ovxVvPjNL7qsZF7nTEUsgWgKZet7hKWnH-gfzNVISQEoNXAhx58mbNSbqunggZy4sXx5b2w9WIiC83HMiMVVlpPsToRdPXzWsxKx71vIORSsc3g8Jkv0H8ZUs05z22ZO0joz1xfCJGyuBnm4xjpxtbgfKqALdvtq3YzL-zpDnF3DPmAMihuMp-ZJeulQZhbwsLPmPrh4ZwtX17CtUKDhzvm0xDTRUqzwBQ3A__&Key-Pair-Id=APKAITJV77WS5ZT7262A',
 'description': 'C# 2017 비주얼 프로그래밍을 능숙하게 활용하기!',
 'instructor': 'ITGO 아이티고',
 'course_link': 'https://www.udemy.com/course/hdc-uxmg/',
 'chapter_list': [{'chapter': 'C# 기초부터 윈도우 프로그램까지 Part.120 lectures•7hr 48min',
   'section': ['VS 2017 설치, Hello C# 프로그램 작성 -1Preview24:32',
    'VS 2017 설치, Hello C# 프로그램 작성 -226:45',
    'VS 2017 설치, Hello C# 프로그램 작성 -313:01',
    '변수, 자료형, 값형식과 참조형식, 주석문, 형변환, 열거식, 기타형식 -123:02',
    '변수, 자료형, 값형식과 참조형식, 주석문, 형변환, 열거식, 기타형식 -221:22',
    '변수, 자료형, 값형식과 참조형식, 주석문, 형변환, 열거식, 기타형식 -331:36',
    '변수, 자료형, 값형식과 참조형식, 주석문, 형변환, 열거식, 기타형식 -423:59',
    '연산자, 연산자 우선순위 -122:30',
    '연산자, 연산자 우선순위 -220:48',
    '연산자, 연산자 우선순위 -325:24',
    '연산자, 연산자 우선순위 -425:47',
    '조건문, 반복문 -119:23',
    '조건문, 반복문 -223:19',
    '조건문, 반복문 -327:09',
    '메서드, 매개변수 전달 방식 -115:26',
    '메서드, 매개변수 전달 방식 -221:17',
    '메서드, 매개변수 전달 방식 -326:31',
    'OOP, 클래스, 생성자, 소멸자, 상속, 오버라이딩, 복사 -123:48',
    'OOP, 클래스, 생성자, 소멸자, 상속, 오버라이딩, 복사 -225:50',
    'OOP, 클래스, 생성자, 소멸자, 상속, 오버라이딩, 복사 -327:00']},
  {'chapter': 'C# 기초부터 윈도우 프로그램까지 Part.217 lectures•6hr 43min',
   'section': ['접근제한자, 구조체, 인터페이스, 추상클래스 -1Preview31:01',
    '접근제한자, 구조체, 인터페이스, 추상클래스 -219:12',
    '접근제한자, 구조체, 인터페이스, 추상클래스 -323:06',
    '프로퍼티, 배열, 컬렉션 -126:50',
    '프로퍼티, 배열, 컬렉션 -231:24',
    '프로퍼티, 배열, 컬렉션 -323:14',
    '프로퍼티, 배열, 컬렉션 -423:53',
    '프로퍼티, 배열, 컬렉션 -514:20',
    '인덱서, out24:35',
    '제네릭 프로그래밍 -119:55',
    '제네릭 프로그래밍 -226:30',
    '예외처리 -121:57',
    '예외처리 -219:35',
    'GUI 프로그래밍 -119:28',
    'GUI 프로그래밍 -224:32',
    'GUI 프로그래밍 -321:52',
    'GUI 프로그래밍 -431:22']}]}]

course_info_save(data, site)

