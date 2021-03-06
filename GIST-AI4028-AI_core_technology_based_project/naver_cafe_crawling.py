# -*- coding: UTF-8 -*-
# author : Jihun Jeung (jihun@gm.gist.ac.kr)

# !pip install bs4
# !pip install requests
# !pip install selenium
# ! pip install pyperclip

# # chromedrive in colab
# !apt-get update
# !apt install chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin

import requests as req # to bring the HTML information from a web
from bs4 import BeautifulSoup as bs # to parsing HTML
import pandas as pd 
from selenium import webdriver
import time 
import pyperclip


import time
from selenium import webdriver
import csv
import random
from bs4 import BeautifulSoup as bs # to parsing HTML
from tqdm import tqdm

PRINT= False
NUM_PAGES= 5
# naver_login()
# time.sleep(35)

# chromedrive in Colab
options = webdriver.ChromeOptions()
options.add_argument('--headless')        # Head-less 설정
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=options)

# crawling
total_list = []
URL = 'https://cafe.naver.com/bezzeraclub?iframe_url=/ArticleList.nhn%3Fsearch.clubid=22853449%26search.boardtype=L%26search.totalCount=151%26search.cafeId=22853449%26search.page='
for i in tqdm(range(NUM_PAGES)): #스크래핑 할 페이지수 
    pg = str(i+1) 
    addr = URL+pg 
    driver.get(addr) # access to address
    driver.switch_to.frame('cafe_main') # look up a 'cafe_main' frame
    html = driver.page_source # read html
    soup = bs(html, 'html.parser') # html parser
    
    a_article_list, a_writer_list, a_regdate_list, a_linkname_list, strong_boardtag_list = [], [], [], [], []
    a_article_list = soup.findAll("a",{"class":"article"})
        # a_article_list[0].string # title
        # a_article_list[0]['href'] # URL
    a_writer_list = soup.findAll("a",{"class":"m-tcol-c"})  # writer
    a_regdate_list = soup.findAll("td",{"class":"td_date"}) # date
    a_linkname_list = soup.findAll("a",{"class":"link_name"})
        # a_linkname_list[0].string # board title
    strong_boardtag_list = soup.findAll("strong",{"class":"board-tag-txt"}) # to remove notification
    remove_str_on_title_head = '\n                                \n                                \n\n                                \n                                \n\n                                \n                                \n                                    \n                                    '
    remove_str_on_title_tail = '\n                                    \n                                \n                            '
    
    
    if i==0 : # notice
        assert len(a_article_list) == len(a_writer_list) == len(a_regdate_list) == len(strong_boardtag_list) + len(a_linkname_list)
    
        for index in range(len(strong_boardtag_list), len(a_article_list)):
            sub_list = []
            sub_list.append(str(a_article_list[index].string).replace(remove_str_on_title_head, '').replace(remove_str_on_title_tail, '')) # title without remove_str_on_title
            sub_list.append("https://cafe.naver.com" +str(a_article_list[index]['href'])) # URL
            sub_list.append(a_writer_list[index].string) # writer
            sub_list.append(a_regdate_list[index].string) # writing data
            sub_list.append(a_linkname_list[index-len(strong_boardtag_list)].string) # board title
    

            # chromedrive setting for colab
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome('chromedriver', options=options)
            
            # content scrapping
            adrs = "https://cafe.naver.com" +str(a_article_list[index]['href'])
            driver.get(adrs) 
            time.sleep(1+random.uniform(0, 1)) 
            driver.switch_to.frame('cafe_main') 
            html = driver.page_source 
            soup = bs(html, 'html.parser') 

            article_content_list = soup.findAll("span",{"class":"se-fs- se-ff- "})
            contents = ''
            for index in range(len(article_content_list)):
                contents += str(article_content_list[index].string) + ' '
            sub_list.append(contents) # article contents
            if PRINT: print(adrs) 


            total_list.append(sub_list) 

    else:
        assert len(a_article_list) == len(a_writer_list) == len(a_regdate_list) == len(a_linkname_list)
    
        for index in range(len(a_article_list)):
            sub_list = []
            sub_list.append(str(a_article_list[index].string).replace(remove_str_on_title_head, '').replace(remove_str_on_title_tail, '')) # title without remove_str_on_title
            sub_list.append("https://cafe.naver.com" +str(a_article_list[index]['href'])) # URL
            sub_list.append(a_writer_list[index].string) # writer
            sub_list.append(a_regdate_list[index].string) # writing data
            sub_list.append(a_linkname_list[index-len(strong_boardtag_list)].string) # board title


            # chromedrive setting for colab
            options = webdriver.ChromeOptions()
            options.add_argument('--headless') 
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome('chromedriver', options=options)

            # content scrapping
            adrs = "https://cafe.naver.com"+str(a_article_list[index]['href'])
            driver.get(adrs) 
            time.sleep(1+random.uniform(0, 1)) 
            driver.switch_to.frame('cafe_main') 
            html = driver.page_source 
            soup = bs(html, 'html.parser') 
            
            contents = ''
            article_content_list = soup.findAll("span",{"class":"se-fs- se-ff- "})
            for index in range(len(article_content_list)):
                contents += str(article_content_list[index].string) + ' '
            sub_list.append(contents) # article contents
            if PRINT: print(adrs) 

            total_list.append(sub_list)

driver.close()

# to save crawling data
f = open(f'naver_cafe_crawling.csv','w',encoding='utf-8',newline='')  
csvWriter = csv.writer(f)
for i in total_list: 
    csvWriter.writerow(i) 
f.close() 
print("완료 !")
