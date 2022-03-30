import pandas as pd
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
import pickle

# exclude those earning call which is not valid
articles = pd.read_csv('./data/locations.csv')
articles = articles[articles['Children'] == False]
articles = articles[articles['Company'] != 'WMT']
articles = articles[articles['Company'] != 'GOOGL']
articles.dropna(inplace=True)

articles.sort_values(by=['Company', 'Date'], inplace=True)
articles.reset_index(drop=True, inplace=True)

# read innovation dictionary
terms_set = pd.read_csv('./data/innovation_short.csv', index_col=0)
terms_set.dropna(inplace=True)
terms_set['word'] = terms_set['word'].apply(str.lower)
ps = PorterStemmer()
terms_set['word'] = terms_set['word'].apply(ps.stem)

no_stops = pickle.load(open('./data/no_stops_words.p', 'rb'))

# count the innovation for each article
v_arr = []
for article in no_stops:
    article = [ps.stem(w) for w in article]
    terms_count = []
    for terms in terms_set['word']:
        count = article.count(terms)
        terms_count.append(article.count(terms)) 
    terms_count.extend([sum(terms_count), len(article), sum(terms_count) / len(article)])
    v_arr.append(terms_count)

c = terms_set['word'].to_list()
c.extend(['sum', 'total', 'ratio'])
v_df = pd.DataFrame(v_arr, columns=c)
pd.concat([articles[['Date', 'Company']], v_df], axis=1).to_csv('./data/innovation_number.csv')