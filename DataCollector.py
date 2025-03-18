from WebScraper import HTMLParser, ExtractText, DataSaver
import time
import csv
import os

def ErrorStorer(idx):
    with open("error.txt", "a") as f:
        f.write(f"Error at index: {idx}\n")

def ParseAndAdd(url,filename,idx):
    soup=HTMLParser.get_soup(url)
    dataList=ExtractText.get_para(soup,bangla_only=True)
    if dataList==[]:
        ErrorStorer(i)
        print("No Bangla text found...")
        return
    heading=ExtractText.get_tags(soup, ["h1"], min_length=1, bangla_only=True)
    try:
        startingparser="<#START-ASTHA#> "+heading[0]
    except Exception as e:
        startingparser="<#START-ASTHA#> Heading not found"
        print(f"Heading not found...")
    endingparser="<#END-ASTHA#>"
    dataList.insert(0,startingparser)
    dataList.append(endingparser)
    DataSaver.save_csv(dataList, filename, append=True, source_url=url)

baseUrl="https://www.bd-pratidin.com/national/2025/03/18/"


print("Please, see the last line of the csv file and enter the starting index. Careful with the index, it may generate repeated data.")
start_index=input("Please, enter the starting index: ")
start_index=int(start_index)+1
for i in range(start_index, 1000000):
    try:
        ParseAndAdd(baseUrl+str(i), "trainData.csv",i)
    except Exception as e:
        ErrorStorer(i)
        print(f"Error at {i}: {e}")
    time.sleep(1)