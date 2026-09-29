import requests
import time
import json
import os
from datetime import datetime


# HackerNews API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Identify our application to the API
headers = {
    "User-Agent": "TrendPulse/1.0"
}


# Keywords used to classify stories
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


def get_category(title):
    """
    Check the title against our keyword lists.
    Matching is case-insensitive.
    """

    title_lower = title.lower()

    # TODO:
    # Loop through each category and its keywords.
    # If a keyword is found in the title,
    # return that category.
    #
    # If nothing matches, return None.

    pass


# ---------------------------------------------------------
# Step 1: Get the top 500 story IDs
# ---------------------------------------------------------

try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    story_ids = response.json()[:500]

    print(f"Found {len(story_ids)} story IDs.")

except requests.RequestException as error:
    print(f"Failed to fetch story IDs: {error}")
    story_ids = []


# ---------------------------------------------------------
# Step 2: Fetch individual story details
# ---------------------------------------------------------

stories = []

for story_id in story_ids:

    try:
        url = ITEM_URL.format(story_id)

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        story = response.json()

        # Some IDs may not contain usable story data.
        if story and story.get("title"):
            stories.append(story)

    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        continue


print(f"Successfully fetched {len(stories)} stories.")


# ---------------------------------------------------------
# Step 3: Categorise stories
# ---------------------------------------------------------

collected_stories = []

# Keep track of how many stories we have in each category.
category_counts = {
    category: 0 for category in categories
}


# ---------------------------------------------------------
# Step 4: Save the collected stories
# ---------------------------------------------------------

os.makedirs("data", exist_ok=True)

today = datetime.now().strftime("%Y%m%d")

filename = f"data/trends_{today}.json"


with open(filename, "w", encoding="utf-8") as file:
    json.dump(collected_stories, file, indent=4)


print(
    f"Collected {len(collected_stories)} stories. "
    f"Saved to {filename}"
)
