import pandas as pd

df = pd.read_csv("Posts_Raw.csv")
df = df.assign(Post_url='https://www.reddit.com'+df['Original_Post'])
JudgementForm = []
for a in range(len(df['JudgementForm'].tolist())):
    JudgementForm.append([item.replace("'","") for item in df['JudgementForm'].tolist()[a][1:-1].split(", ")][2:])
for a in range(len(JudgementForm)):
    temp = []
    for b in range(len(JudgementForm[a])):
        temp.append(JudgementForm[a][b].split(" "))
    JudgementForm[a]=temp
for a in range(len(JudgementForm)):
    for b in range(1,len(JudgementForm[a])):
        JudgementForm[a][b]=JudgementForm[a][b][1:]
for a in range(len(JudgementForm)):
    temp=[]
    temp.append(JudgementForm[a][len(JudgementForm[a])-1][-2])
    temp.insert(0, 'top comment')
    JudgementForm[a][len(JudgementForm[a])-1]=temp
print(JudgementForm[1])
df['JudgementForm']= JudgementForm
df.drop('Unnamed: 0', axis=1, inplace=True)
df.drop('Original_Post', axis=1, inplace=True)
df.to_csv('Post_Cleaned.csv')
