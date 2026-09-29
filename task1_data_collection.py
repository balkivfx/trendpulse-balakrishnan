import os
import sys
import time
import json
import requests
from datetime import datetime

# Define the targeted categories and their exact case-insensitive keywords
CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def determine_category(title):
    """
    Evaluates a story title against the keyword dictionary.
    Returns the first matching category name (lower case match), or None.
    """
    if not title:
        return None
        
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return None

def main():
    # Setup required request headers to identify the application
    headers = {"User-Agent": "TrendPulse/1.0"}
    
    # ----------------------------------------------------
    # STEP 1: Fetch Top Story IDs
    # ----------------------------------------------------
    top_stories_url = "https://firebaseio.com"
    print("Fetching top story IDs from HackerNews...")
    
    try:
        response = requests.get(top_stories_url, headers=headers, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:500]  # Limit ingestion to the first 500 IDs
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch top stories: {e}")
        sys.exit(1)

    # Dictionary buckets to collect up to 25 items per target domain
    collected_by_category = {cat: [] for cat in CATEGORIES}
    total_collected_count = 0
    
    # ----------------------------------------------------
    # STEP 2: Processing & API loops
    # ----------------------------------------------------
    # We iterate sequentially through categories as instructed.
    # To satisfy "one sleep per category loop, not per individual story",
    # we run the heavy parsing loop grouped by category structures.
    for category in CATEGORIES:
        print(f"Processing category: '{category}'...")
        
        for story_id in story_ids:
            # Enforce capacity ceiling restriction per category bucket
            if len(collected_by_category[category]) >= 25:
                break
                
            item_url = f"https://firebaseio.com{story_id}.json"
            
            try:
                item_res = requests.get(item_url, headers=headers, timeout=5)
                if item_res.status_code != 200:
                    continue
                
                story_data = item_res.json()
                if not story_data or story_data.get("type") != "story":
                    continue
                
                title = story_data.get("title", "")
                assigned_cat = determine_category(title)
                
                # Check if this specific story fits our active loop category
                if assigned_cat == category:
                    extracted_story = {
                        "post_id": story_data.get("id"),
                        "title": title,
                        "category": category,
                        "score": story_data.get("score", 0),
                        "num_comments": story_data.get("descendants", 0),
                        "author": story_data.get("by", "unknown"),
                        "collected_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                    }
                    collected_by_category[category].append(extracted_story)
                    total_collected_count += 1
                    
            except requests.exceptions.RequestException:
                # Catch failures cleanly without crashing the script execution pipeline
                continue
        
        # Enforce the required 2-second timeout delay between category sweeps
        time.sleep(2)

    # Flatten out compiled lists into a single payload matrix
    all_stories = []
    for cat_list in collected_by_category.values():
        all_stories.extend(cat_list)

    # ----------------------------------------------------
    # STEP 3: Save results to structured JSON
    # ----------------------------------------------------
    # Generate targeted paths dynamically using standard dates
    os.makedirs("data", exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    output_filename = f"data/trends_{date_str}.json"
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_stories, f, indent=4, ensure_ascii=False)
        
    print(f"Collected {total_collected_count} stories. Saved to {output_filename}")

if __name__ == "__main__":
    main()
