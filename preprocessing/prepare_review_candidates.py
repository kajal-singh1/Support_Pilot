
import pandas as pd
import re

# 1. Load the original dataset
df = pd.read_csv("data/tickets.csv")

# 2. Keep English tickets only
df = df[df["language"] == "en"].copy()

# 3. Handle missing values
df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")

# 4. Combine subject and description
df["ticket_text"] = (
    df["subject"].astype(str) + " " +
    df["body"].astype(str)
).str.lower()

# 5. Define search patterns
search_patterns = {
    "VPN": [
        r"\bvpn\b",
        r"\bvirtual private network\b"
    ],
    "Password": [
        r"\bpassword\b",
        r"\bpasscode\b",
        r"\bcredentials?\b"
    ]
}

# 6. Prepare tag columns
tag_columns = [f"tag_{i}" for i in range(1, 9)]

for col in tag_columns:
    df[col] = (
        df[col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

# 7. Collect candidate tickets
review_rows = []

for category, patterns in search_patterns.items():

    combined_pattern = "|".join(patterns)

    mask = df["ticket_text"].str.contains(
        combined_pattern,
        regex=True,
        na=False
    )

    matches = df[mask].copy()

    for index, row in matches.iterrows():

        # Check whether the exact category tag exists
        has_exact_tag = any(
            row[col] == category.lower()
            for col in tag_columns
        )

        # Find the keywords matched in the ticket
        matched_terms = re.findall(
            combined_pattern,
            row["ticket_text"]
        )

        review_rows.append({
            "ticket_id": index,
            "candidate_category": category,
            "subject": row["subject"],
            "description": row["body"],
            "queue": row["queue"],
            "priority": row["priority"],
            "matched_keywords": ", ".join(set(matched_terms)),
            "has_exact_tag": has_exact_tag,
            "reviewed_category": ""
        })

# 8. Convert results into a DataFrame
review_df = pd.DataFrame(review_rows)

# 9. Save the review file
review_df.to_csv(
    "data/review_candidates.csv",
    index=False
)

print("Review candidate file created successfully!")
print("Total candidate records:", len(review_df))

print("\nCandidates by category:")
print(review_df["candidate_category"].value_counts())

print("\nExact tag distribution:")
print(
    review_df.groupby(
        ["candidate_category", "has_exact_tag"]
    ).size()
)

print("\nSaved to: data/review_candidates.csv")
