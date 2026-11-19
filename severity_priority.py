import re

# 1. Predict severity from ticket description
def predict_severity(description):

    text = description.lower()

    critical_words = [
        "server down",
        "entire company",
        "production down",
        "security breach"
    ]

    high_keywords = [
    "urgent",
    "cannot work",
    "business stopped",
    "client meeting",
    "vpn not working",
    "vpn is not working",
    "cannot access company resources",
    ]

    medium_words = [
        "slow",
        "error",
        "problem",
        "issue"
    ]

    if any(word in text for word in critical_words):
        return "Critical"

    elif any(word in text for word in high_keywords):
        return "High"

    elif any(word in text for word in medium_words):
        return "Medium"

    else:
        return "Low"


# 2. Calculate priority using severity and business impact
def calculate_priority(severity, business_impact):

    severity = severity.capitalize()
    business_impact = business_impact.capitalize()

    if severity == "Critical" and business_impact == "High":
        return "P1"

    elif severity == "High" and business_impact == "High":
        return "P1"

    elif severity == "High":
        return "P2"

    elif severity == "Medium":
        return "P3"

    else:
        return "P4"


# 3. Test the functions
if __name__ == "__main__":

    description = "Production down. Entire company cannot work."

    severity = predict_severity(description)

    business_impact = "High"

    priority = calculate_priority(
        severity,
        business_impact
    )

    print("Ticket Description:", description)
    print("Severity:", severity)
    print("Business Impact:", business_impact)
    print("Priority:", priority)
