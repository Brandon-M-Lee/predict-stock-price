import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd
from urllib import parse

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')  
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')

company_list = list(pd.read_csv('stock_code.csv', encoding='cp949')['종목명'])

def get_article_links(company):
    article_links = list()
    for i in range(400):
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={parse.quote(company)}&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=28&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={i}1'
        
        driver.get(url)
        article_links += [i.get_attribute('href') for i in driver.find_elements(By.TAG_NAME, 'a') if i.text=='네이버뉴스']

    return article_links

def get_content(url):
    driver.get(url)