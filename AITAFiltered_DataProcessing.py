import pandas as pd

df = pd.read_csv("Posts_Raw.csv")
df = df.assign(Post_url='https://www.reddit.com'+df['Original_Post'])
print(df['JudgementForm'])