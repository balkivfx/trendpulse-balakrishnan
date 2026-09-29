import pandas as pd
from pathlib import Path

# ---------------------------------------------
# 1. Load the JSON file
# ---------------------------------------------

# Find the JSON file created by Task 1
data_folder = Path("data")
json_files = list(data_folder.glob("trends_*.json"))

if not json_files:
    print("No TrendPulse JSON file found in the data folder.")
    exit()

input_file = json_files[0]

# Load JSON into a DataFrame
df = pd.read_json(input_file)

print(f"Loaded {len(df)} stories from {input_file}")


# ---------------------------------------------
# 2. Clean the data
# ---------------------------------------------

# Remove duplicate stories based on post_id
df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")


# Remove rows where post_id, title, or score is missing
df = df.dropna(subset=["post_id", "title", "score"])

print(f"After removing nulls: {len(df)}")


# Make score and num_comments integers
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# Remove rows where score could not be converted
df = df.dropna(subset=["score"])

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)


# Remove stories with score less than 5
df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")


# Remove extra spaces from titles
df["title"] = df["title"].str.strip()


# ---------------------------------------------
# 3. Save the cleaned data
# ---------------------------------------------

output_file = data_folder / "trends_clean.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")


# ---------------------------------------------
# Stories per category
# ---------------------------------------------

print("\nStories per category:")
print(df["category"].value_counts())
