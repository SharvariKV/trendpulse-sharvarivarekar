import pandas as pd
import json
import os

file_path="data/trends_20260409.json"

with open(file_path,"r",encoding="utf-8") as f:
    data=json.load(f)

print(f"Loaded {len(data)} stories from {file_path}")

df=pd.DataFrame(data)

df=df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")

df=df.drop_duplicates(subset=["post_id","title","score"])
print(f"After removing nulls: {len(df)}")

df["score"]=df["score"].astype(int)
df["num_comments"]=df["num_comments"].fillna(0).astype(int)

df=df[df["score"]>=5]
print(f"After removing low scores: {len(df)}")

df["title"]=df["title"].str.strip()

if not os.path.exists("data"):
    os.makedirs("data")

output_file="data/trends_clean.csv"
df.to_csv(output_file,index=False)

print(f"\nSaved {len(df)} rows to {output_file}")
print(f"\nStories per category:")
print(df["category"].value_counts())
