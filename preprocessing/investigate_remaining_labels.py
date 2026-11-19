
import pandas as pd

df = pd.read_csv("data/tickets.csv")

# Keep English-language tickets
df = df[df["language"] == "en"].copy()

categories = ["network", "software", "hardware"]
tag_columns = [f"tag_{i}" for i in range(1, 9)]

# Clean tag values
for col in tag_columns:
    df[col] = df[col].fillna("").astype(str).str.strip().str.lower()

for category in categories:

    matches = df[df[tag_columns].eq(category).any(axis=1)]

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

        print(
            "Tags:",
            [row[col] for col in tag_columns if row[col]]
        )
