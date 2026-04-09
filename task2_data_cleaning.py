import pandas as pd
import json
import os

file_path="data/trends_20260409.json"

with open(file_path,"r",encoding="utf-8") as f:
    data=json.load(f)

print("Loaded JSON data")
print("Number of records:", len(data))

df=pd.DataFrame(data)

df=df.drop_duplicates(subset=["post_id"])

df=df.dropna(subset=["title"])

df["score"]=df["score"].fillna(0)
df["num_comments"]=df["num_comments"].fillna(0)

df["score"]=df["score"].astype(int)
df["num_comments"]=df["num_comments"].astype(int)

if not os.path.exists("data"):
    os.makedirs("data")

output_file="data/cleaned_trends.csv"
df.to_csv(output_file,index=False)

print(f"Cleaned data saved to {output_file}")
print(f"Total records: {len(df)}")