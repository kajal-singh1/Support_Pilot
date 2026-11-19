import pandas as pd
import re

# Load original dataset
df = pd.read_csv("data/tickets.csv")

# Keep English tickets
df = df[df["language"] == "en"].copy()

# Combine subject and body
df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")

df["ticket_text"] = (
    df["subject"] + " " + df["body"]
).str.lower()

# Category identification patterns
patterns = {
    "VPN": [
        r"\bvpn\b"
    ],
    "Password": [
        r"reset.{0,25}password",
        r"password.{0,25}(reset|expired|forgot|change)",
        r"forgot.{0,15}password",
        r"password.{0,15}(login|access)",
        r"unable to log in",
        r"cannot log in"
    ],
    "Network": [
        r"\bwi-fi\b",
        r"\bwifi\b",
        r"\binternet connection\b",
        r"\bnetwork connectivity\b",
        r"\bnetwork connection\b",
        r"\brouter\b"
    ],
    "Hardware": [
        r"\bprinter\b",
        r"\bkeyboard\b",
        r"\bmonitor\b",
        r"\bmouse\b",
        r"\bheadset\b",
        r"\bhardware\b",
        r"\bscanner\b"
    ],
    "Software": [
        r"\bsoftware installation\b",
        r"\binstalling software\b",
        r"\bapplication error\b",
        r"\bsoftware update\b",
        r"\bapplication installation\b",
        r"\bsoftware\b"
    ],
    "System": [
        r"\boperating system\b",
        r"\bsystem downtime\b",
        r"\bsystem crash\b",
        r"\bserver down\b",
        r"\bboot failure\b"
    ]
}

# Assign one preliminary category
def assign_category(text):

    for category, expressions in patterns.items():

        for expression in expressions:

            if re.search(expression, text):
                return category

    return None


df["category"] = df["ticket_text"].apply(assign_category)

# Keep only tickets with a category
training_df = df.dropna(subset=["category"]).copy()

# Keep useful columns
training_df = training_df[
    ["subject", "body", "category", "priority", "queue"]
]

# Save separate training dataset
training_df.to_csv(
    "data/training_tickets.csv",
    index=False
)

print("\nTRAINING DATASET CREATED")
print("-" * 40)

print("Total English tickets:", len(df))
print("Selected training tickets:", len(training_df))

print("\nCategory distribution:")
print(training_df["category"].value_counts())

print("\nPriority distribution:")
print(training_df["priority"].value_counts())

print("\nSaved: data/training_tickets.csv")
