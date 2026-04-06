import requests
import json
import os
from datetime import datetime

# -----------------------------
# API endpoints (Hacker News)
# -----------------------------
top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"   # returns list of top story IDs
item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"     # returns details of each story

# Adding a header (good practice, avoids request blocking sometimes)
headers = {"User-Agent": "TrendPulse/1.0"}

# -----------------------------
# Keywords for categorization
# -----------------------------
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# -----------------------------
# Function to assign category based on title
# -----------------------------
def get_category(title):
    title = title.lower()  # convert to lowercase for easy matching

    # loop through each category and its keywords
    for category, words in categories.items():
        for word in words:
            if word in title:   # if keyword found in title
                return category

    # if nothing matches, classify as 'others'
    return "others"


# -----------------------------
# Step 1: Fetch top story IDs
# -----------------------------
res = requests.get(top_url, headers=headers)
story_ids = res.json()

# Only take first 500 stories (as per assignment)
story_ids = story_ids[:500]


# -----------------------------
# Step 2: Fetch details for each story
# -----------------------------
data = []   # this will store all story records

for sid in story_ids:
    try:
        # request story details using ID
        r = requests.get(item_url.format(sid), headers=headers)
        story = r.json()

        # skip if data is invalid or title is missing
        if not story or "title" not in story:
            continue

        title = story["title"]

        # create a structured dictionary for each story
        record = {
            "post_id": story.get("id"),                        # unique story ID
            "title": title,                                    # story title
            "category": get_category(title),                   # category based on keywords
            "score": story.get("score", 0),                    # upvotes
            "num_comments": story.get("descendants", 0),       # number of comments
            "author": story.get("by", "unknown"),              # author name
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # timestamp
        }

        # add record to list
        data.append(record)

    except:
        # skip if any error occurs for a story
        continue


# -----------------------------
# Step 3: Save data to JSON file
# -----------------------------
# create 'data' folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# fixed filename (so it doesn't change every run)
filename = "data/trends.json"

# write data into JSON file
with open(filename, "w") as f:
    json.dump(data, f, indent=4)

# final message
print(f"Collected {len(data)} stories. Saved to {filename}")
