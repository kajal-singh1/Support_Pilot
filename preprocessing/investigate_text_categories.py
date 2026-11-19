
import pandas as pd

# Load the existing dataset
df = pd.read_csv("data/tickets.csv")

# Keep English tickets only
df = df[df["language"] == "en"].copy()

# Combine subject and body for searching
df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")

df["ticket_text"] = (
    df["subject"].astype(str) + " " +
    df["body"].astype(str)
).str.lower()

# Search patterns for potential VPN and Password tickets
search_patterns = {
    "VPN": [
        r"\bvpn\b",
        r"\bvirtual private network\b"
    ],

    "Password": [
        r"\bpassword\b",
        r"\bpasscode\b",
        r"\bforgot my password\b",
        r"\breset password\b",
        r"\bcredentials?\b"
    ]
}

# Clean tag columns
tag_columns = [f"tag_{i}" for i in range(1, 9)]

for col in tag_columns:
    df[col] = (
        df[col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

# Investigate each category
for category, patterns in search_patterns.items():

    # Find tickets matching any search pattern
    mask = df["ticket_text"].str.contains(
        "|".join(patterns),
        regex=True,
        na=False
    )

    matches = df[mask].copy()

    # Check whether the matching category tag exists
    tagged_mask = matches[tag_columns].eq(
        category.lower()
    ).any(axis=1)

    tagged_count = tagged_mask.sum()
    untagged_count = (~tagged_mask).sum()

    print("\n" + "=" * 60)
    print("CATEGORY:", category)
    print("=" * 60)

    print("Text-matching tickets:", len(matches))
    print("Matching tickets with exact tag:", tagged_count)
    print("Matching tickets without exact tag:", untagged_count)

    print("\n--- SAMPLE TICKETS WITHOUT EXACT TAG ---")

    untagged = matches[~tagged_mask]

    for index, row in untagged.head(10).iterrows():

        print("\nTicket ID:", index)
        print("Subject:", row["subject"])
        print("Description:", row["body"][:400])
        print("Queue:", row["queue"])
        print("Priority:", row["priority"])

        print(
            "Tags:",
            [row[col] for col in tag_columns if row[col]]
        )
