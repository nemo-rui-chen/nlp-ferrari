from bs4 import BeautifulSoup
import os

comp_list = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'BRK.B', 'NVDA', 'FB', 'V', 'UNH', 'JNJ', 'JPM', 'WMT', 'PG', 'BAC', 'MA', 'XOM', 'HD', 'CVX', 'DIS', 'KO', 'PFE', 'ABBV', 'AVGO', 'CSCO', 'COST', 'PEP', 'LLY', 'VZ', 'ADBE', 'NKE', 'TMO', 'ABT', 'CMCSA', 'CRM', 'WFC', 'ORCL', 'AMD', 'ACN', 'DHR', 'INTC', 'QCOM', 'MRK', 'UPS', 'MCD', 'NFLX', 'T', 'MS', 'SCHW']

for comp in comp_list:
    old_dir = f'./articles/{comp}'
    new_dir = f'./pure_articles/{comp}'
    if os.path.exists(new_dir) == False:
        os.mkdir(new_dir)
    for filename in os.listdir(old_dir):
        f = open(os.path.join(old_dir, filename), 'r')
        page = BeautifulSoup(f, 'html.parser')
        paragraphs = page.find('div', {'data-test-id':'content-container'})
        out_f = open(os.path.join(new_dir, filename), 'w')
        out_f.write(str(paragraphs))
        out_f.close()
    