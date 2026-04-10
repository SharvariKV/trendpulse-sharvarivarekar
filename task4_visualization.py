print("Program started")

import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = "data/trends_analysed.csv"

df = pd.read_csv(file_path)

if not os.path.exists("outputs"):
    os.makedirs("outputs")

top_stories = df.sort_values(by="score", ascending=False).head(10)

top_stories["short_title"] = top_stories["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure(figsize=(8, 6))
plt.barh(top_stories["short_title"], top_stories["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()
plt.savefig("outputs/chart1_top_stories.png")

category_counts = df["category"].value_counts()

plt.figure(figsize=(6, 5))
plt.bar(category_counts.index, category_counts.values, color=["red","green","orange","purple"])
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.xticks(rotation=30)
plt.savefig("outputs/chart2_categories.png")

plt.figure(figsize=(6, 5))

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
plt.savefig("outputs/chart3_scatter.png")

fig, axs = plt.subplots(1, 3, figsize=(18,5))

axs[0].barh(top_stories["short_title"], top_stories["score"])
axs[0].set_title("Top Stories")
axs[0].invert_yaxis()

axs[1].bar(category_counts.index, category_counts.values)
axs[1].set_title("Categories")

axs[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axs[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axs[2].set_title("Score vs Comments")
axs[2].legend()

fig.suptitle("TrendPulse Dashboard")
plt.savefig("outputs/dashboard.png")

print("All charts saved in 'outputs/' folder")