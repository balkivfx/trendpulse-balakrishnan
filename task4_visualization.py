import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------
# 1. Load data and setup
# ---------------------------------------------

# Load the analysed data from Task 3
df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder if it does not exist
output_folder = Path("outputs")
output_folder.mkdir(exist_ok=True)


# ---------------------------------------------
# 2. Chart 1 — Top 10 Stories by Score
# ---------------------------------------------

# Select the 10 stories with the highest scores
top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

# Highest score should appear at the top
plt.gca().invert_yaxis()

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

plt.tight_layout()

# Save before show
plt.savefig(output_folder / "chart1_top_stories.png")

plt.show()
plt.close()


# ---------------------------------------------
# 3. Chart 2 — Stories per Category
# ---------------------------------------------

category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))

# Each category gets a different colour automatically
plt.bar(
    category_counts.index,
    category_counts.values
)

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.xticks(rotation=30)

plt.tight_layout()

# Save before show
plt.savefig(output_folder / "chart2_categories.png")

plt.show()
plt.close()


# ---------------------------------------------
# 4. Chart 3 — Score vs Comments
# ---------------------------------------------

plt.figure(figsize=(9, 6))

# Non-popular stories
not_popular = df[df["is_popular"] == False]

# Popular stories
popular = df[df["is_popular"] == True]

plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.legend()

plt.tight_layout()

# Save before show
plt.savefig(output_folder / "chart3_scatter.png")

plt.show()
plt.close()


# ---------------------------------------------
# 5. Bonus — TrendPulse Dashboard
# ---------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Chart 1 inside dashboard
axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)

axes[0, 0].invert_yaxis()
axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")


# Chart 2 inside dashboard
axes[0, 1].bar(
    category_counts.index,
    category_counts.values
)

axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")
axes[0, 1].tick_params(axis="x", rotation=30)


# Chart 3 inside dashboard
axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)

axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")
axes[1, 0].legend()


# Remove unused fourth subplot
fig.delaxes(axes[1, 1])

# Overall dashboard title
fig.suptitle("TrendPulse Dashboard", fontsize=18)

plt.tight_layout()

# Save dashboard
plt.savefig(output_folder / "dashboard.png")

plt.show()
plt.close()


print("\nAll charts saved successfully!")
print("Output folder:", output_folder)
