from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import  BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import tempfile

A = time.time()



driver = webdriver.Chrome()
url = 'https://www.youtube.com/watch?v=ZoZ7eWAe0dg'
driver.get(url)

time.sleep(2)

last_height = driver.execute_script("return document.documentElement.scrollHeight")
click_number = 10

while click_number > 0:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    click_number -= 1
    if new_height == last_height:
        break
    last_height = new_height


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
comments = []
containers = soup.find_all("ytd-comment-thread-renderer", class_="style-scope ytd-item-section-renderer")
for idx, container in enumerate(containers):
    span = container.find("span", class_="yt-core-attributed-string yt-core-attributed-string--white-space-pre-wrap")
    author = container.find("a", id="author-text")
    author_href = container.find("a",class_="yt-simple-endpoint style-scope ytd-comment-view-model").get("href")
    href_link = "https://youtube.com"+ author_href
    likes_num = container.find("span",id="vote-count-middle")

    # likes = 
    if span and author:
        comments.append([span.text.strip(),author.text.strip(),href_link,likes_num.text.strip()])
    else:
        print("없ㄴㄴㄷ?")

df = pd.DataFrame(comments, columns=["작성자", "댓글","주소","좋아요수"])
df.to_excel(f'{i.split("?"[1])}.xlsx', index=False, engine='openpyxl')

B = time.time()

print(B-A)