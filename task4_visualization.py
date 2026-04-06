import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------------
# 1 — Setup
# ---------------------------

# Load dataset
df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder if not exists
os.makedirs("outputs", exist_ok=True)


# shorten titles
def shorten_title(title, max_len=50):
    return title if len(title) <= max_len else title[:47] + "..."
df["short_title"] = df["title"].apply(shorten_title)

# ---------------------------
# 2 — Chart 1: Top 10 Stories by Score
# ---------------------------

top10 = df.sort_values(by="score", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()  # highest score on top

plt.savefig("outputs/chart1_top_stories.png")
plt.show()

# ----------------------------------------
# 3 — Chart 2: Stories per Category
# ----------------------------------------

cat_counnt = df['category'].value_counts()
colors = ['red', 'blue', 'green', 'orange','purple'] # Define a list of colors for each bar

plt.figure(figsize=(10,6))
plt.bar(cat_counnt.index, cat_counnt.values, color=colors)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.savefig("outputs/chart2_categories.png")
plt.show()

# ---------------------------
# 4 — Chart 3: Score vs Comments
# ---------------------------

plt.figure(figsize=(10, 6))

# Separate popular and non-popular
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["num_comments"], popular["score"], label="Popular")
plt.scatter(not_popular["num_comments"], not_popular["score"], label="Not Popular")

plt.xlabel("Number of Comments")
plt.ylabel("Score")
plt.title("Score vs Comments")
plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.show()


# ---------------------------
# BONUS — Dashboard
# ---------------------------

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# ---- Chart 1: Top Stories ----
axes[0].barh(top10["short_title"], top10["score"])
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()

# ---- Chart 2: Categories ----
axes[1].bar(cat_counnt.index, cat_counnt.values, color = colors)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")

# ---- Chart 3: Scatter ----
axes[2].scatter(popular["num_comments"], popular["score"], label="Popular")
axes[2].scatter(not_popular["num_comments"], not_popular["score"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Comments")
axes[2].set_ylabel("Score")
axes[2].legend()

# ---- Overall title ----
fig.suptitle("TrendPulse Dashboard", fontsize=16)

plt.tight_layout()

# Save BEFORE show
plt.savefig("outputs/dashboard.png")
plt.show()

print("✅ Dashboard created successfully!")