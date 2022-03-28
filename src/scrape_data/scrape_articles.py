import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import random
import pandas as pd
import requests
import os

url = 'https://seekingalpha.com{}'

#comp_list = ['CMCSA']
comp_list = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'BRK.B', 'NVDA', 'FB', 'V', 'UNH', 'JNJ', 'JPM', 'WMT', 'PG', 'BAC', 'MA', 'XOM', 'HD', 'CVX', 'DIS', 'KO', 'PFE', 'ABBV', 'AVGO', 'CSCO', 'COST', 'PEP', 'LLY', 'VZ', 'ADBE', 'NKE', 'TMO', 'ABT', 'CMCSA', 'CRM', 'WFC', 'ORCL', 'AMD', 'ACN', 'DHR', 'INTC', 'QCOM', 'MRK', 'UPS', 'MCD', 'NFLX', 'T', 'MS', 'SCHW']
#browser = webdriver.Chrome('/Users/nemo/miniforge3/bin/chromedriver')

# print(ua.safari)

# driver = webdriver.Safari()
# driver.get(url)

#opt = webdriver.ChromeOptions()
#browser = webdriver.Chrome()

option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches",['enable-automation'])
option.add_argument("disable-blink-features=AutomationControlled")
# ua = UserAgent()
# option.add_argument('user-agent={}'.format(ua.safari))

#browser = webdriver.Chrome(options=option)

def deal_one_article(article, comp):
    # browser.get(url.format(article['link']))
    # text = browser.find_element(By.XPATH, '//*[@id="content"]/div/div/article'
    title = article['title'].replace('/', '_')
    if article['type'] != 'transcript' or \
        (article['title'].find('Earnings Call Transcript') == -1 and \
            article['title'].find('Earnings Calls Transcript') == -1 and \
            article['title'].find('Earning Call Transcript') == -1 and \
            article['title'].find('Earnings Conference Call') == -1 and \
            article['title'].find('Earnings Call') == -1) or \
        article['title'].find('Webcast') != -1 or \
        pd.Timestamp(article['date']).tz_convert(None) < pd.Timestamp('2011-01-01'):
        return
    file_path = f"./articles/{comp}/{article['date']}_{title}.html"
    if os.path.isfile(file_path):
        return

    sleep(random.randint(1, 3)) 
    page = requests.get(url.format(article['link']))
    text = page.text 
    out_file = open(f"./articles/{comp}/{article['date']}_{title}.html", 'w')
    out_file.write(text)
    out_file.close()
    print(file_path)

for comp in comp_list:
    print(comp)
    if os.path.isdir(f'./articles/{comp}') == False:
        os.mkdir(f'./articles/{comp}')
    artilce_list = pd.read_csv('./article_list/{}_articles.csv'.format(comp))
    artilce_list.apply(deal_one_article, axis=1, comp=comp)

