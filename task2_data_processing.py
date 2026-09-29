import pandas as pd
import numpy as np

# --------------------------------------------------
# 1. Load and Explore
# --------------------------------------------------

# Load the cleaned data from Task 2
df = pd.read_csv("data/trends_clean.csv")

# Print dataset shape
print("Loaded data:", df.shape)

# Print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Calculate average score and average comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print("\nAverage score   :", average_score)
print("Average comments:", average_comments)


# --------------------------------------------------
# 2. Basic Analysis with NumPy
# --------------------------------------------------

# Convert score column to NumPy array
scores = df["score"].to_numpy()

# NumPy statistics
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

# Highest and lowest scores
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print("Mean score   :", mean_score)
print("Median score :", median_score)
print("Std deviation:", std_score)
print("Max score    :", max_score)
print("Min score    :", min_score)


# Find the category with the most stories
category_counts = df["category"].value_counts()

most_category = category_counts.idxmax()
most_category_count = category_counts.max()

print(
    "\nMost stories in:",
    most_category,
    f"({most_category_count} stories)"
)


# Find the story with the most comments
most_commented_index = df["num_comments"].idxmax()

most_commented_title = df.loc[most_commented_index, "title"]
most_commented_count = df.loc[most_commented_index, "num_comments"]

print(
    '\nMost commented story:',
    f'"{most_commented_title}" — {most_commented_count} comments'
)


# --------------------------------------------------
# 3. Add New Columns
# --------------------------------------------------

# Engagement = comments per score
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# True if score is greater than average score
df["is_popular"] = df["score"] > average_score


# --------------------------------------------------
# 4. Save the Analysed Data
# --------------------------------------------------

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print("\nSaved to", output_file)
