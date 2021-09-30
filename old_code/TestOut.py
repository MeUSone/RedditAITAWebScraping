import praw
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import ast

load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    user_agent="my user agent",
    username=os.environ.get("username"),
    password=os.environ.get("password")
)


df = pd.read_csv("Post.csv")
def cleanForm(cleanText):
    cleanText = ast.literal_eval(cleanText)
    JudgementForm = {}
    for a in range(len(cleanText)-1):
        JudgementForm[cleanText[a][0]] = float(cleanText[a][1].strip('%'))/100
    return JudgementForm
#Difference between custmized algorithm and flair
print(sum(df["Same Label"]))


temp = []
for a in range( len(df["JudgementForm"])):
    data = list(cleanForm(df["JudgementForm"][a]).items())
    data = sorted(data, key=lambda x: x[1], reverse=True)
    temp.append(data[0][0])

#Difference between custmized algorithm and judgement form
temp1 = []
for a in range(len(df)):
    temp1.append(ast.literal_eval(df["Custom Score"][a])[0][0] == temp[a])
print(sum(temp1))

#Difference between judgement form and flair
temp2 =[]
abbreviation_form={" Not the A-hole":"NTA"," Asshole":"YTA"," Not Enough Info":"INFO"," Everyone Sucks":"ESH"," No A-holes":"NAH"}
for a in range(len(df)):
    temp2.append(temp[a] == abbreviation_form.get(df["FinalResult"][a]))
print(sum(temp2))