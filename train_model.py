import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. Load training dataset
df = pd.read_csv("data/training_tickets.csv")

# 2. Prepare text and labels
df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")

X = df["subject"] + " " + df["body"]
y = df["category"]

# 3. Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# 4. Create TF-IDF + Logistic Regression pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            max_features=10000,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        )
    )
])

# 5. Train model
print("\nTraining model...")

model.fit(X_train, y_train)

# 6. Predict test records
y_pred = model.predict(X_test)

# 7. Evaluate model
accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL EVALUATION")
print("----------------------------")

print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# 8. Save trained model
joblib.dump(model, "models/ticket_classifier.pkl")

print("\nModel saved successfully!")
print("Location: models/ticket_classifier.pkl")
