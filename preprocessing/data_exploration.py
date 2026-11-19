import pandas as pd
from pathlib import Path

# Locate the dataset
file_path = Path("data") / "tickets.csv"

# Load CSV using Pandas
df = pd.read_csv(file_path)

# 1. Dataset dimensions
print("\n--- DATASET SHAPE ---")
print("Rows and Columns:", df.shape)

# 2. Column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

# 3. First five records
print("\n--- FIRST FIVE RECORDS ---")
print(df.head())

# 4. Dataset information
print("\n--- DATASET INFORMATION ---")
df.info()

# 5. Missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 6. Language distribution
print("\n--- LANGUAGE DISTRIBUTION ---")
print(df["language"].value_counts())

# 7. Priority distribution
print("\n--- PRIORITY DISTRIBUTION ---")
print(df["priority"].value_counts())

# 8. Existing ticket categories
print("\n--- QUEUE DISTRIBUTION ---")
print(df["queue"].value_counts())

print("\nDataset exploration completed!")


# 9. Filter English tickets
english_df = df[df["language"] == "en"].copy()

print("\n--- ENGLISH DATASET ---")
print("English records:", len(english_df))

# 10. Display sample ticket descriptions
print("\n--- SAMPLE TICKETS ---")

for index, row in english_df.head(10).iterrows():

    print("\nTicket:", index)
    print("Subject:", row["subject"])
    print("Description:", row["body"][:300])
    print("Queue:", row["queue"])
    print("Priority:", row["priority"])

    print("Tags:", [
        row[f"tag_{i}"]
        for i in range(1, 9)
        if pd.notna(row[f"tag_{i}"])
    ])

# 11. Check unique ticket types
print("\n--- TICKET TYPES ---")
print(english_df["type"].value_counts())

# 12. Check tag_1 distribution
print("\n--- TOP 20 TAGS ---")
print(english_df["tag_1"].value_counts().head(20))


