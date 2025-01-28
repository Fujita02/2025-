# SeleniumのWebDriverをインポート
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
import time

#requestsとBeautiful Soup のインポート
import requests 
from bs4 import BeautifulSoup
#csvのインポート
import csv
#datetimeのインポート
import datetime

# Google Chromeを起動
driver = webdriver.Chrome()

# Googleトップページを開く
driver.get('https://google.com/')

# 検索窓を探索する
el = driver.find_element(By.NAME,'q')
# 検索名を入力
el.send_keys('ニュース')
# 検索フォーム送信
el.submit()

time.sleep(20)

# リンクを探す
element = driver.find_element(By.PARTIAL_LINK_TEXT,'news.yahoo.co.jp')
# リンクをクリックする
element.click()

url = "https://news.yahoo.co.jp/"
res = requests.get(url)
soup = BeautifulSoup(res.content, "html.parser")

today = soup.find("section", attrs ={"id":"uamods-topics"})

# 記事のタイトルとURLがある部分を抽出
entries = today.find_all("li")
# CSV出力用リスト
today_list = []
index = 1

# 情報を取得する
for entry in entries:
    # "li"の箇所のタイトルに該当するテキスト（ページ上の文章）を取得
    title = entry.get_text()
    # "li"の箇所のURLを取得
    entry_url = entry.find("a").get("href")
    # 出力用リストにタイトルとURLを格納  
    today_list.append([index, title ,entry_url])
    # インデックスをインクリメント
    index += 1 

print(today_list)

#結果をCSVファイルに書き出し。ファイル名は現在時刻
with open('_NewsTopics.csv', 'w')as file:
    writer=csv.writer(file,lineterminator='\n')
    writer.writerows(today_list)
#soup = BeautifulSoup(res.text, "html.parser")
#import re

#elems = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
#elems

#for elem in elems:
#    print(elem.contents[0])
#    print(elem.attrs['href'])

#10秒待って閉じる
time.sleep(10)
driver.close()