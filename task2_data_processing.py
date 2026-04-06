import pandas as pd
import os

# -----------------------------
# Step 1: Load the latest JSON file
# -----------------------------

# Folder where our JSON files are stored
file_path = "data"

# Get all JSON files in the folder
files = [f for f in os.listdir(file_path) if f.endswith(".json")]

# Pick the latest file (sorted by name/date)
latest_file = sorted(files)[-1]

# Read JSON file into pandas DataFrame
df = pd.read_json(os.path.join(file_path, latest_file))

print(f"Loaded {len(df)} stories from {latest_file}")


# -----------------------------
# Step 2: Data Cleaning
# -----------------------------

# Remove duplicate entries based on post_id
# (Sometimes same story may appear multiple times)
df = df.drop_duplicates(subset="post_id")
print("After removing duplicates:", len(df))

# Drop rows where important values are missing
# (We need post_id, title, and score at minimum)
df = df.dropna(subset=["post_id", "title", "score"])
print("After removing nulls:", len(df))

# Convert score and number of comments to integers
# (Sometimes they may be treated as float or object)
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low-quality posts (very low score)
# Keeping only somewhat popular ones
df = df[df["score"] >= 5]
print("After removing low scores:", len(df))

# Clean titles by removing unwanted spaces at beginning/end
df["title"] = df["title"].str.strip()


# -----------------------------
# Step 3: Save cleaned data
# -----------------------------

# Output file path
output_file = "data/trends_clean.csv"

# Save DataFrame as CSV file
df.to_csv(output_file, index=False)

print(f"Saved {len(df)} rows to {output_file}")


# -----------------------------
# Step 4: Quick summary
# -----------------------------

# Show how many stories fall into each category
print("\nStories per category:")
print(df["category"].value_counts())