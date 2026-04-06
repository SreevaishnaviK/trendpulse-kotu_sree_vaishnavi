import requests          # To make API requests
import time              # (Optional here) used for delays if needed
import json              # To handle JSON data
import os                # To work with files/folders
from datetime import datetime   # To get current date & time

# -----------------------------
# API URLs (Hacker News)
# -----------------------------
top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"   # Gives top story IDs
item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"     # Gives details of each story

# -----------------------------
# Header (good practice for API calls)
# -----------------------------
headers = {"User-Agent": "TrendPulse/1.0"}

# -----------------------------
# Categories with keywords
# Used to classify news based on title
# -----------------------------
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# -----------------------------
# Function to assign category
# Checks if any keyword exists in title
# -----------------------------
def get_category(title):
    title = title.lower()   # Convert to lowercase for matching
    for category, words in categories.items():
        for word in words:
            if word in title:   # If keyword found → return category
                return category
    return "others"   # Default category if no match

# -----------------------------
# Fetch top story IDs
# -----------------------------
try:
    res = requests.get(top_url, headers=headers)  # API call
    story_ids = res.json()                        # Convert response to list
except:
    print("Error fetching top stories")
    story_ids = []

# -----------------------------
# Initialize storage
# -----------------------------
data = []   # To store final results

# Track how many stories per category
category_count = {key: 0 for key in categories}

# -----------------------------
# Fetch each story details
# -----------------------------
for sid in story_ids:
    try:
        # Get story details using ID
        r = requests.get(item_url.format(sid), headers=headers)
        story = r.json()

        # Skip if invalid or missing title
        if not story or "title" not in story:
            continue

        title = story["title"]

        # Assign category based on title
        category = get_category(title)

        # Limit: max 25 stories per category
        if category in category_count and category_count[category] >= 25:
            continue

        # Increment category count
        if category in category_count:
            category_count[category] += 1

        # Create structured record
        record = {
            "post_id": story.get("id"),                         # Story ID
            "title": title,                                     # Story title
            "category": category,                               # Assigned category
            "score": story.get("score", 0),                     # Upvotes
            "num_comments": story.get("descendants", 0),        # Number of comments
            "author": story.get("by", "unknown"),               # Author name
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
        }

        # Add record to data list
        data.append(record)

        # Stop after collecting ~125 stories total
        if len(data) >= 125:
            break

    except:
        print("Error fetching story", sid)
        continue

# -----------------------------
# Create folder if not exists
# -----------------------------
if not os.path.exists("data"):
    os.makedirs("data")

# -----------------------------
# Save data as JSON file
# -----------------------------
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w") as f:
    json.dump(data, f, indent=4)   # Save formatted JSON

# -----------------------------
# Final output message
# -----------------------------
print(f"Collected {len(data)} stories. Saved to {filename}")
