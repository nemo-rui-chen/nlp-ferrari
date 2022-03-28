import pandas as pd
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
import pickle

articles = pd.read_csv('./data/locations.csv')
articles = articles[articles['Children'] == False]
articles = articles[articles['Company'] != 'WMT']
articles = articles[articles['Company'] != 'GOOGL']
articles.dropna(inplace=True)

articles.sort_values(by=['Company', 'Date'], inplace=True)
articles.reset_index(drop=True, inplace=True)

terms_set = pd.read_csv('./data/innovation_short.csv', index_col=0)
terms_set.dropna(inplace=True)
terms_set['word'] = terms_set['word'].apply(str.lower)
ps = PorterStemmer()
terms_set['word'] = terms_set['word'].apply(ps.stem)

no_stops = pickle.load(open('./data/no_stops_words.p', 'rb'))

v_arr = []
for article in no_stops:
    article = [ps.stem(w) for w in article]
    terms_count = []
    for terms in terms_set['word']:
        count = article.count(terms)
        #if count != 0:
            #print(path, terms, count)
        terms_count.append(article.count(terms)) 
    terms_count.extend([sum(terms_count), len(article), sum(terms_count) / len(article)])
    #print(terms_count)
    #break
    v_arr.append(terms_count)

c = terms_set['word'].to_list()
c.extend(['sum', 'total', 'ratio'])
v_df = pd.DataFrame(v_arr, columns=c)
pd.concat([articles[['Date', 'Company']], v_df], axis=1).to_csv('./data/innovation_number.csv')

# def deal_one_article(row):
#     if pd.isna(row['Path']) :
#         return [0 for _ in range(len(terms_set))]
#     path = './data' + row['Path']
#     article = open(path, 'r').read().lower()
#     terms_count = []
#     for terms in terms_set['word']:
#         count = article.count(terms)
#         #if count != 0:
#             #print(path, terms, count)
#         terms_count.append(article.count(terms))
#     return terms_count
    

#all_terms_count = articles[articles['Company'] == 'AAPL'].apply(deal_one_article, axis=1, result_type='expand')
# all_terms_count = articles.apply(deal_one_article, axis=1, result_type='expand')
# all_terms_count.rename(columns=dict(zip(range(len(terms_set)), terms_set['word'])), inplace=True)
# all_terms_count['sum'] = all_terms_count.apply(lambda row: row.sum(), axis=1)


# pd.concat([articles[['Date', 'Company']], all_terms_count], axis=1).to_csv('./data/innovation_number.csv')