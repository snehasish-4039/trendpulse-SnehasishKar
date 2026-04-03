##imports----
import requests
import time
from datetime import datetime
import json
import os
##-----------


##configs--------------------------------------
BASE_URL = "https://hacker-news.firebaseio.com/v0"

HEADERS = {"User-Agent": "TrendPulse/1.0"}

CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}
##---------------------------------------------


##functions for easy applications----------------------
def get_top_story_ids():
    url = f"{BASE_URL}/topstories.json"
    response = requests.get(url, headers=HEADERS)
    return response.json()[:500]

def get_story_details(story_id):
    try:
        url = f"{BASE_URL}/item/{story_id}.json"
        response = requests.get(url, headers=HEADERS)
        return response.json()
    except:
        print(f"Failed to fetch story {story_id}")
        return None

def categorize(title):
    title_lower = title.lower()
    
    for category, keywords in CATEGORIES.items():
        for word in keywords:
            if word in title_lower:
                return category
    return "other"
##------------------------------------------------




##----main logic------
def collect_stories():
    story_ids = get_top_story_ids()
    category_counts = {cat: 0 for cat in CATEGORIES}
    collected = []

    for story_id in story_ids:
        story = get_story_details(story_id)

        if not story or "title" not in story:
            continue

        category = categorize(story["title"])

        if category not in category_counts:
            continue

        if category_counts[category] >= 25:
            continue

        story_data = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected.append(story_data)
        category_counts[category] += 1

        # Sleep after each successful addition (acceptable approximation)
        time.sleep(2)

        # Stop when all categories reach limit
        if all(count >= 25 for count in category_counts.values()):
            break

    return collected

##save function----------------
def save_to_json(data):
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Collected {len(data)} stories. Saved to {filename}")


#  RUN

if __name__ == "__main__":
    all_stories = collect_stories()
    save_to_json(all_stories)