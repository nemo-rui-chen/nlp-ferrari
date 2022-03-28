from doctest import DocFileTest
import pandas as pd
from fuzzywuzzy import fuzz
import os
from bs4 import BeautifulSoup
from nltk import sent_tokenize
import numpy as np

# To give score to a specific event of an earning call using fuzzy match
def score(df,i,path):
    scorels = []
    temp =df.iloc[i]
    word = temp.word
    filePath = temp.Path
    filePath = path+filePath
    file = open(filePath,"r") 
    text = "".join(file.readlines())
    soup = BeautifulSoup(text,"html.parser")
    # Only get text information
    text = soup.text
    sentences = sent_tokenize(text)
    for sentence in sentences:
        scorels.append(fuzz.partial_ratio(word,sentence))
    score = np.mean(scorels)
    file.close()
    df.loc[i,"score"] = score

def main():
    # Load the data
    articles = pd.read_csv("locations.csv")
    headlines = pd.read_csv("headlines_processed.csv")
    headlines = headlines[["word",'year']]
    # Get the year information
    articles["year"] = articles["Date"].apply(lambda x:int(x.split("Q")[0]))
    df = pd.merge(articles,headlines,on="year")
    path = os.getcwd()
    df["score"] = 0
    # Only focus on the company itself
    df = df[df["Children"]==False].dropna()
    df = df.reset_index()
    # Score each event of each EC
    for i in range(len(df)):
        score(df,i,path)
    # Average all the Event scores of an EC, and get the final event score for an EC
    df["CompanyDate"] = df["Company"]+" "+ df["SpecificDate"]
    df = df.groupby(df["CompanyDate"]).mean()
    df["CompanyDate"] = df.index
    df["Company"] = df["CompanyDate"].apply(lambda x:x.split()[0])
    df["Date"] = df["CompanyDate"].apply(lambda x:x.split()[1])
    df = df[["Company","Date","score"]].reset_index()
    # Normalize the event score feature
    df['score'] = (df["score"]-df["score"].mean())/df["score"].std()
    df = df.iloc[:,1:]
    df.to_csv("event.csv",index=False)

main()



