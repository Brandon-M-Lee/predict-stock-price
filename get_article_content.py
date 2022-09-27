import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd
from urllib import parse
import datetime

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')  
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')

company_list = list(pd.read_csv('stock_code.csv', encoding='cp949')['종목명'])

def get_article_links(company, driver):
    article_links = list()
    for i in range(1):
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={parse.quote(company)}&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=28&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={i}1'
        
        driver.get(url)
        article_links += [i.get_attribute('href') for i in driver.find_elements(By.TAG_NAME, 'a') if i.text=='네이버뉴스']

    return article_links

def get_info(url, driver):
    driver.get(url)
    content = driver.find_element(By.ID, 'dic_area').text
    datetime_ = driver.find_element(By.CLASS_NAME, 'media_end_head_info_datestamp_time _ARTICLE_DATE_TIME').text
    if '오전' in datetime_:
        if len(datetime_) == 19:
            datetime_ = datetime.datetime.strptime(datetime_.replace('오전 ', 'AM 0'), '%Y.%m.%d. %p %I:%M')
        elif len(datetime_) ==20:
            datetime_ = datetime.datetime.strptime(datetime_.replace('오전', 'AM'), '%Y.%m.%d. %p %I:%M')
    elif '오후' in datetime_:
        if len(datetime_) == 19:
            datetime_ = datetime.datetime.strptime(datetime_.replace('오후 ', 'PM 0'), '%Y.%m.%d. %p %I:%M')
        if len(datetime_) == 20:
            datetime_ = datetime.datetime.strptime(datetime_.replace('오후', 'PM'), '%Y.%m.%d. %p %I:%M')
    
    return content, datetime_

def save_data(company, driver):
    article_links = get_article_links(company, driver)
    with open(f'data/{company}_article_data.csv', 'w') as f:
        f.write('내용, 날짜\n')
        for article_link in article_links:
            content, datetime_ = get_info(article_link, driver)
            f.write(f'{content}, {datetime_}\n')

if __name__ == '__main__':
    for company in company_list:
        save_data(company, driver)