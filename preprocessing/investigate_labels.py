
import pandas as pd

# Load original dataset
df = pd.read_csv("data/tickets.csv")

# Keep English records
df = df[df["language"] == "en"].copy()

# Categories we need to investigate
target_categories = ["vpn", "password", "system"]

# Combine all eight tag columns
tag_columns = [f"tag_{i}" for i in range(1, 9)]

# Normalize tags for comparison
for col in tag_columns:
    df[col] = df[col].fillna("").astype(str).str.strip().str.lower()

print("\n--- CATEGORY INVESTIGATION ---")

for category in target_categories:

    # Find records containing the exact category tag
    mask = df[tag_columns].eq(category).any(axis=1)

    matches = df[mask]

    print("\n" + "=" * 60)
    print("CATEGORY:", category.upper())
    print("Matching records:", len(matches))
    print("=" * 60)

    for index, row in matches.head(5).iterrows():

        print("\nTicket ID:", index)
        print("Subject:", row["subject"])
        print("Description:", row["body"][:500])

        print("Queue:", row["queue"])
        print("Priority:", row["priority"])

        print("Tags:", [
            row[col] for col in tag_columns if row[col]
        ])
