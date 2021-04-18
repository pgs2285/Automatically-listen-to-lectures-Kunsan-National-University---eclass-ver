from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

import time
from tqdm import tqdm

def login(StudentID, Password):

    driver.find_element_by_xpath("//*[@id='login_popup']").click()
    driver.find_element_by_xpath("//*[@id='userDTO.userId']").send_keys(StudentID)
    driver.find_element_by_xpath('//*[@id="userDTO.password"]').send_keys(Password)
    driver.find_element_by_xpath('//*[@id="loginForm"]/a').click()

def classSearch(num):
    time.sleep(1)
    driver.find_element_by_class_name("sb-toggle-left").click()
    className = driver.find_element_by_xpath(f"html/body/nav/div/fieldset/select/option[{num}]").click()
    driver.implicitly_wait(1)

def checkAlert():
    time.sleep(10)
    try:  
        alert = driver.switch_to.alert.accept()
    except:
        pass

def classLearning(week):
#/html/body/main/form/div[3]/section/div[2]/div/div[5]/div/table/
#/html/body/main/form/div[3]/section/div[2]/div/div[4]/div/h3/i
    
    url = driver.current_url
    driver.get(url)
    innerBox = driver.find_element_by_xpath(f'/html/body/main/form/div[3]/section/div[2]/div/div[{week}]/div/table')        
    elements = innerBox.find_elements_by_class_name('bar-gray')
    elements2 = innerBox.find_elements_by_class_name('bar-orange')
    elements += elements2
    for i in range(len(elements)-1, -1, -1): #강의 개수만큼 돈다
       
        driver.get(url)
        innerBox = driver.find_element_by_xpath(f'/html/body/main/form/div[3]/section/div[2]/div/div[{week}]/div/table')        
        elements = innerBox.find_elements_by_class_name('bar-gray')
        elements2 = innerBox.find_elements_by_class_name('bar-orange')
        elements += elements2

        try:
            elements[i].find_element_by_xpath('./../../../li[3]/a').send_keys('\n')
        except:
            continue

        checkAlert()
        time.sleep(1)    
        try:
            iframes = driver.find_element_by_xpath("//*[@id='bodyFrame']")
            driver.switch_to.frame(iframes)
            time.sleep(1)
            playButton = driver.find_element_by_class_name('vjs-big-play-button').click()
            time.sleep(5)
            left_time = driver.find_element_by_class_name('vjs-remaining-time-display').get_attribute("innerHTML")
            print(left_time)
            min, sec = left_time.split(':')
 
            for i in tqdm(range(int(min)*60 + int(sec))):
                time.sleep(1)
            time.sleep(1)
            driver.switch_to.default_content()
            driver.find_element_by_xpath("//*[@id='frameBox']/div[2]/a").send_keys('\n')
            time.sleep(1)
        except:
            print("강의 수강 오류발생 - 다시시도.")    

            try:
                try:
                    driver.switch_to.default_content()
                except:
                    pass    
                driver.find_element_by_xpath("//*[@id='frameBox']/div[2]/a").send_keys('\n')
                time.sleep(1)
            except:
                pass

print("크롬드라이브 버전을 현재 크롬 버전과 맞춰주세요.")
StudentID = input('StudentID:')
Password = input("StudentPW:")
week = input("이번주 주차를 입력해주세요:")
driver = webdriver.Chrome('./chromedriver')
url = 'https://eclass.kunsan.ac.kr/MMain.do?cmd=viewIndexPage&userDTO.localeKey=ko'
driver.get(url)

#로그인 하기
try:
    login(StudentID, Password)
except:
    print("로그인실패 다시시도해주세요")
    driver.close()      

#수강하는 강의 목록, 개수 불러오기
try:
    for i in range(2,15):
        time.sleep(1)
        classSearch(str(i))
        classLearning(week)
        #bar-orange 이거나 bar-gray일 경우에 click후 학습 시작
except:
    print("프로그램 종료합니다 - j.s.park")
    driver.close()
