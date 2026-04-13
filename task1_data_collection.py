import requests
import json
import os
import time
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Category keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 25


# -----------------------------
# FUNCTION: Get Top Story IDs
# -----------------------------
def get_top_story_ids():
    try:
        url = f"{BASE_URL}/topstories.json"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:500]  # First 500
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


# -----------------------------
# FUNCTION: Get Story Details
# -----------------------------
def get_story(story_id):
    try:
        url = f"{BASE_URL}/item/{story_id}.json"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


# -----------------------------
# FUNCTION: Categorize Story
# -----------------------------
def categorize(title):
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None


# -----------------------------
# MAIN SCRIPT
# -----------------------------
def main():
    story_ids = get_top_story_ids()

    collected = {cat: [] for cat in CATEGORIES.keys()}
    all_stories = []

    for story_id in story_ids:
        story = get_story(story_id)

        if not story or "title" not in story:
            continue

        category = categorize(story["title"])

        if category and len(collected[category]) < MAX_PER_CATEGORY:
            data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected[category].append(data)
            all_stories.append(data)

            print(f"Added [{category}] - {story.get('title')}")

        # Stop if all categories filled
        if all(len(collected[c]) >= MAX_PER_CATEGORY for c in CATEGORIES):
            break

    # Sleep AFTER each category loop (requirement)
    for _ in CATEGORIES:
        time.sleep(2)

    # -----------------------------
    # SAVE JSON
    # -----------------------------
    os.makedirs("data", exist_ok=True)

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_stories, f, indent=4)

    print(f"\nCollected {len(all_stories)} stories. Saved to {filename}")


# Run script
if __name__ == "__main__":
    main()
