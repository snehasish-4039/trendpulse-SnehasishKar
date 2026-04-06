import pandas as pd 
import numpy as np
df=pd.read_csv("data/trends_clean.csv")
# -------------------------------------
# 1 — Load and Explore
# -------------------------------------
print(f"loaded data : {df.shape}")
print("First 5 row: \n", df.head(10).to_string(index=False))

#getting average score and comments 
avg_score= round(df['score'].mean(),2)
avg_num_comments= round(df['num_comments'].mean(),2)

print(f"\nAverage score   : {avg_score}")
print(f"Average comments: {avg_num_comments}")

# ----------------------------------------
# 2 — Basic Analysis with NumPy
# ----------------------------------------
scores = df['score'].values

#calculating scores using numpy
mean_score = round(np.mean(scores),2)
median_score = round(np.median(scores),2)
st_deviation = round(np.std(scores),2)
max_score = round(np.max(scores),2)
min_score = round(np.min(scores),2) 

print("\n--- NumPy Stats ---\n")
print(f"Mean score  : {mean_score}")
print(f"Median score: {median_score}")
print(f"Std deviation: {st_deviation}")
print(f"Max score   : {max_score}")
print(f"Min score   : {min_score}")

# -------------------------------
# Category with most stories
# -------------------------------

category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")


# -------------------------------
# Most commented story
# -------------------------------

most_commented = df.loc[df["num_comments"].idxmax()]

print(
    f'\nMost commented story: "{most_commented["title"]}" — {most_commented["num_comments"]} comments')


# -------------------------------
# 3 — Add New Columns
# -------------------------------

df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > mean_score

# -------------------------------
# 4 — Save the Result
# -------------------------------

sav_path = "data/trends_analysed.csv"
df.to_csv(sav_path, index=False)

print(f"\nSaved to {sav_path}")