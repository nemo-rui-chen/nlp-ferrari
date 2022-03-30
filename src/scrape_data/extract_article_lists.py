'''
Extracting the URL list from Json data file
'''
import json
import pandas as pd
import os

comp_list = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'BRK.B', 'NVDA', 'FB', 'V', 'UNH', 'JNJ', 'JPM', 'WMT', 'PG', 'BAC', 'MA', 'XOM', 'HD', 'CVX', 'DIS', 'KO', 'PFE', 'ABBV', 'AVGO', 'CSCO', 'COST', 'PEP', 'LLY', 'VZ', 'ADBE', 'NKE', 'TMO', 'ABT', 'CMCSA', 'CRM', 'WFC', 'ORCL', 'AMD', 'ACN', 'DHR', 'INTC', 'QCOM', 'MRK', 'UPS', 'MCD', 'NFLX', 'T', 'MS', 'SCHW']

for comp in comp_list:
    articles = []
    print(comp)
    for i in range(10):
        if os.path.isfile('./original_article_lists/{}_{}data.json'.format(comp, i)) == False:
            break
        in_file = open('./original_article_lists/{}_{}data.json'.format(comp, i), 'r')
        j = json.load(in_file)
        for article in j['data']:
            articles.append([article['type'], article['attributes']['title'], article['links']['self'], article['attributes']['publishOn']])
        in_file.close()
    print(len(articles))
    pd.DataFrame(articles, columns=['type', 'title', 'link', 'date']).to_csv('./article_list/{}_articles.csv'.format(comp))