import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import random

url = 'https://seekingalpha.com/symbol/V/earnings/transcripts'
url = 'https://seekingalpha.com/api/v3/symbols/{}/transcripts?filter[until]={}&id={}&include=author%2CprimaryTickers%2CsecondaryTickers%2Csentiments&isMounting=true&page[size]=200'

comp_list = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'BRK.B', 'NVDA', 'FB', 'V', 'UNH', 'JNJ', 'JPM', 'WMT', 'PG', 'BAC', 'MA', 'XOM', 'HD', 'CVX', 'DIS', 'KO', 'PFE', 'ABBV', 'AVGO', 'CSCO', 'COST', 'PEP', 'LLY', 'VZ', 'ADBE', 'NKE', 'TMO', 'ABT', 'CMCSA', 'CRM', 'WFC', 'ORCL', 'AMD', 'ACN', 'DHR', 'INTC', 'QCOM', 'MRK', 'UPS', 'MCD', 'NFLX', 'T', 'MS', 'SCHW']
comp_list = []
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

browser = webdriver.Chrome(options=option)
sleep(10)

for comp in comp_list:
    min_id = 'undefined'
    count = 0
    while (True):
        sleep(random.randint(1, 10))
        sleep(10)
        browser.get(url.format(comp, min_id, comp))
        print(comp)
        try:
            data = browser.find_element(By.TAG_NAME, 'pre')
        except:
            print('fail')
            break
        j = json.loads(data.text)
        try:
            print(len(j['data']))
            if len(j['data']) > 0:
                print(j['data'][-1]['attributes']['title'], j['meta']['page']['minmaxPublishOn'])
        except:
            print('no data')
            break
        out_file = open('./original_article_lists/{}_{}data.json'.format(comp, count), "w")
        json.dump(j, out_file, indent=4)
        out_file.close()
        if len(j['data']) < 50:
            break
        else:
            min_id = j['meta']['page']['minmaxPublishOn']['min']
        count += 1

