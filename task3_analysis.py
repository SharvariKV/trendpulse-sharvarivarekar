print("RUNNING TASK 3")

import pandas as pd
import numpy as np
import os

file_path="data/trends_clean.csv"

df=pd.read_csv(file_path)

print(f"Loaded data: {df.shape}")

print("\nFirst 5 rows:")

print(df.head())

avg_score=df["score"].mean()
avg_comments=df["num_comments"].mean()

print(f"\nAverage score : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")

scores=df["score"].values
comments=df["num_comments"].values

print("\n--- Numpy Stats ---")

print(f"Mean score : {np.mean(scores):.2f}")
print(f"Median score : {np.median(scores):.2f}")
print(f"Std deviation: {np.std(scores):.2f}")

print(f"Max score : {np.max(scores)}")
print(f"Min score : {np.min(scores)}")

category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

max_comments_index = np.argmax(comments)
top_story_title = df.iloc[max_comments_index]["title"]
top_story_comments = df.iloc[max_comments_index]["num_comments"]

print(f"\nMost commented story: \"{top_story_title}\" - {top_story_comments} comments")

df["engagement"] = df["num_comments"] / (df["score"] + 1)

df["is_popular"] = df["score"] > avg_score

if not os.path.exists("data"):
    os.makedirs("data")

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")