import os
import re
import pandas as pd
import numpy as np

# Go through all the files and record the corresponding information
def info_collection():
    df = pd.DataFrame(columns=["Company","Date","Path"])
    originalPath = os.getcwd()
    path = originalPath + os.sep + "pure_articles"
    os.chdir(path)
    companies = os.listdir()
    for company in companies:
        if not company.startswith("."):
            comPath = path + os.sep + company
            os.chdir(comPath)
            fileLs = os.listdir()
            for file in fileLs:
                if not file.startswith("."):
                    date = re.search(r'(\d+\-\d+\-\d+)',file).group()
                    filePath = comPath + os.sep + file
                    filePath = filePath.replace(originalPath,"")
                    df = df.append({"Company":company,"Date":date,"Path":filePath},ignore_index=True)

    os.chdir(originalPath)
    # Save the result into a Dataframe
    df.to_csv("filePath.csv",index = False)

# Get the quarter information from the file nameef getDate(x):
def getDate(x):
    x = re.search(r"(Q\d\s*|F\dQ\s*)\d+",x)
    if x != None:
        return x.group()
# Do some changes to the date information, so that the format is consistent
def dualWithDate(x):
    match = re.match(r'(Q\d)\s*(\d+)',x)
    if match != None:
        quarter = match.group(1)
        year = match.group(2)
        return year + quarter
    else:
        quarter = re.search(r'F(\d)Q',x).group(1)
        year = re.search(r'Q\s*(\d+)',x).group(1)
        if len(year) == 2:
            year = "20"+year
        return year+"Q"+quarter

def data_preprocessing():
    # Get Quarter and Specific Date information from the path of the file
    df = pd.read_csv("filePath.csv")
    df["SpecificDate"] = df["Path"].apply(lambda x: re.search("(\d|\-)+T(\d|\-|\:)+",x).group())
    df["Date"] = df["Path"].apply(getDate)
    df["Date"] = df["Date"].apply(dualWithDate)
    # Build a dictionary to record the ticker - name pairs
    names = pd.read_csv("Top 50 company in S&P500.csv")
    # Clean the data so that it can be mathed properly
    names["Company name "] = names["Company name "].apply(lambda x:re.sub(r"(,*\s*Inc.)","",x))
    names["Company name "] = names["Company name "].apply(lambda x:re.match(r"\w+",x).group())
    names["Ticker"] = names["Ticker"].apply(lambda x:re.sub(r"(\w*:)","",x))
    names["Ticker"] = names["Ticker"].apply(lambda x:re.sub(r"\.","",x))
    names = names.set_index("Ticker")
    nameDic = names["Company name "].to_dict()
    df = df.sort_values(["Date","Company"])
    # Deal with the redundat data and missing data using Children tag
    df["Children"] = False
    companies = df.Company.unique()
    dates = df.Date.unique()
    for date in dates:
        for company in companies:
            # Handle Missing data
            if len(df[(df["Date"]==date) & (df["Company"]==company)]) == 0:
                df = df.append({"Company":company,"Date":date,"Children":False},ignore_index=True)
            # Handle redundant data
            elif len(df[(df["Date"]==date) & (df["Company"]==company)]) > 1:
                temp = df[(df["Date"]==date) & (df["Company"]==company)] 
                condition1 = temp["Path"].str.contains(nameDic[company])==False
                # Companies that have changed their names
                if company == "GOOG" :
                    condition1 = condition1 & (temp["Path"].str.contains("Google")==False)
                elif company == "AVGO":
                    if date <= "2015Q4":
                        condition1 = temp["Path"].str.contains("Avago")==False           
                path = temp["Path"].str.replace("/"+company,"")
                condition2 = True
                # Only consider using Abbreviation to match when the abbreviation is long enough
                if len(company)>=3:
                    condition2 = path.str.contains(company)==False
                condition3 = temp["Path"].str.contains((nameDic[company].capitalize()))==False
                if company == "AVGO":
                    if date <= "2015Q4":
                        condition3 = True
                index = temp[(condition1) & (condition2)&(condition3)].index
                df.loc[index,"Children"]= True
    df = df.sort_values(["Date","Company"]).reset_index(drop=True)
    df.columns = ["Date","Company","Path","SpecificDate","Children"]
    df.loc[:,["Company","Date"]] = df.loc[:,["Date","Company"]].to_numpy()
    # Manually do some informtaion correction for AVGO since it is special
    company = "AVGO"
    date_ls = ["2010Q4","2011Q1","2011Q2","2012Q1"]
    for date in date_ls:
        temp = df[(df["Company"]==company)&(df["Date"]==date)]
        index = temp.index
        df.loc[index,"Children"]=True
        df = df.append({"Company":company,"Date":date,"Children":False},ignore_index=True)
    # Check no missing data
    df1 = df[df["Children"]==False]
    df1 = df1.groupby("Date")['Company'].count()
    print(df1)
    # Check no redundant data
    df1 = df[df.Children == False]
    for date in dates:
        for company in companies:
            if len(df1[(df1["Date"]==date) & (df1["Company"]==company)]) > 1:
                print(company,date)
    df.to_csv("locations.csv",index = False,encoding = "utf_8_sig")


def main():
    info_collection()
    data_preprocessing()

main()