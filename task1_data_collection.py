import requests
import json
import time
from datetime import datetime
import os

TOP_STORIES_URL="https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL="https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

categories={
    "technology":["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews":["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science":["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment":["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def get_category(title):
  title=title.lower()

  for category, keywords in categories.items():
    for keyword in keywords:
      if keyword.lower() in title:
        return category

  return None

try:
    response=requests.get(TOP_STORIES_URL, headers=headers,timeout=10)
    story_ids=response.json()[:500]
    print("Top story IDs fetched successfully.")
except Exception as e:
    print("Error fetching story IDs:",e)
    story_ids=[]

collected_stories=[]

category_count={cat:0 for cat in categories}

for category in categories:
  print(f"\nFetching stories for category: {category}")

  for story_id in story_ids:
    if category_count[category]>=25:
      break

    try:
      url=ITEM_URL.format(story_id)

      for _ in range(2):
        try:
          res=requests.get(url,headers=headers,timeout=10)
          story=res.json()
          break
        except:
          time.sleep(0.2)
      
      else:
        print(f"Error fetching story {story_id}")
        story = None
        continue

      if story is None or "title" not in story:
        continue

      assigned_category=get_category(story["title"])

      if assigned_category==category:

        data={
            "post_id":story.get("id"),
            "title":story.get("title"),
            "category":assigned_category,
            "score":story.get("score",0),
            "num_comments":story.get("descendants",0),
            "author":story.get("by"),
            "collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_stories.append(data)
        category_count[category]+=1
    
    except Exception as e:
      print(f"Error fetching story {story_id}:{e}")
      continue

  time.sleep(0.2)

if not os.path.exists("data"):
   os.makedirs("data")

filename=f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename,"w",encoding="utf-8")as f:
  json.dump(collected_stories,f,indent=4)

print(f"\nCollected {len(collected_stories)} stories.")
print(f"Saved to {filename}")