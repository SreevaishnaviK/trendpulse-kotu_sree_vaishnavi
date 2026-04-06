import pandas as pd
import numpy as np

# -----------------------------
# Step 1: Load the cleaned CSV
# -----------------------------

# Read the cleaned dataset
df = pd.read_csv("data/trends_clean.csv")

print("Loaded data:", df.shape)

# Just to quickly check how the data looks
print("\nFirst 5 rows:")
print(df.head())

# -----------------------------
# Basic statistics
# -----------------------------

# Calculate average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("\nAverage score:", int(avg_score))
print("Average comments:", int(avg_comments))


# -----------------------------
# Step 2: NumPy Analysis
# -----------------------------

# Convert scores column into NumPy array
scores = df["score"].values

print("\n--- NumPy Stats ---")

# Using NumPy for quick statistical calculations
print("Mean score:", int(np.mean(scores)))
print("Median score:", int(np.median(scores)))
print("Std deviation:", int(np.std(scores)))
print("Max score:", int(np.max(scores)))
print("Min score:", int(np.min(scores)))

# -----------------------------
# Category insights
# -----------------------------

# Find which category has the most stories
top_category = df["category"].value_counts().idxmax()
top_count = df["category"].value_counts().max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Find the story with highest number of comments
max_comments_row = df.loc[df["num_comments"].idxmax()]

print(f'Most commented story: "{max_comments_row["title"]}" - {max_comments_row["num_comments"]} comments')


# -----------------------------
# Step 3: Feature Engineering
# -----------------------------

# Create a new column for engagement
# (simple formula: comments relative to score)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Mark stories as popular if score is above average
df["is_popular"] = df["score"] > avg_score


# -----------------------------
# Step 4: Save updated dataset
# -----------------------------

# Save the analysed data into a new CSV file
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")