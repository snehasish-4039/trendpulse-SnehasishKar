##-----imports-----------
import numpy as np
import pandas as pd 
import json
##-----------------------

##-----loading json----------------------
data_json = "data/trends_20260406.json"
df = pd.read_json(data_json)

print(f"loaded {len(df)} stories from {data_json}")
##---------------------------------------


#--removing any row with duplicate post_id----------
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")
##--------------------------------------------------

##------droping rows where post_id, title, or score is missing----------

df = df.dropna(subset=["post_id", "title", "score" ])
print(f"After removing nulls: {len(df)}")


##--------------------------------------------------

##------making score and comment integer type---
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)
##----------------------------------------------


##---remove stories where score is less than 5------

df = df[df["score"] > 5]
print(f"After removing low scores: {len(df)}")
##--------------------------------------------------

#----Strip whitespace from title----------------
df["title"] = df["title"].str.strip()
#----------------------------------------------


# 3 — Save as CSV
save_csv = "data/trends_clean.csv"
df.to_csv(save_csv, index=False)

print(f"\nSaved {len(df)} rows to {save_csv}\n")

##--------summary-------------
print("Stories per category:")
category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"{category:<15} {count}")