
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
import joblib

from database import (
    create_table,
    insert_ticket,
    get_all_tickets,
    get_dashboard_stats,
    update_ticket_status
)

from severity_priority import (
    predict_severity,
    calculate_priority
)

app = Flask(__name__)
app.secret_key = "supportpilot-demo-key"

# Load the existing trained ML model
model = joblib.load("models/ticket_classifier.pkl")

# Create the database table if it does not exist
create_table()


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        employee_name = request.form["employee_name"].strip()
        email = request.form["email"].strip()
        department = request.form["department"].strip()
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        business_impact = request.form["business_impact"]

        ticket_text = title + " " + description

        # ML category prediction
        category = model.predict([ticket_text])[0]

        # Rule-based correction for clear system outages
        system_keywords = [
            "production server down",
            "server down",
            "production down",
            "system downtime",
            "system crash",
            "operating system failure"
        ]

        lower_text = ticket_text.lower()

        if any(keyword in lower_text for keyword in system_keywords):
            category = "System"

        # Rule-based severity prediction
        severity = predict_severity(description)

        # Calculate priority
        priority = calculate_priority(
            severity,
            business_impact
        )

        # Get probability corresponding to the final category
        probabilities = model.predict_proba([ticket_text])[0]
        class_index = list(model.classes_).index(category)
        confidence = float(probabilities[class_index])

        # Insert ticket into SQLite
        insert_ticket(
            employee_name,
            email,
            department,
            title,
            description,
            category,
            severity,
            business_impact,
            priority,
            confidence
        )

        result = {
            "category": category,
            "severity": severity,
            "business_impact": business_impact,
            "priority": priority,
            "confidence": round(confidence * 100, 2)
        }

        flash("Your support ticket has been submitted successfully!", "success")

    # Dashboard statistics
    stats = get_dashboard_stats()

    # Search and filter values
    search = request.args.get("search", "").strip()
    category_filter = request.args.get("category", "")
    priority_filter = request.args.get("priority", "")
    status_filter = request.args.get("status", "")

    tickets = get_all_tickets(
        search,
        category_filter,
        priority_filter,
        status_filter
    )

    return render_template(
        "index.html",
        result=result,
        stats=stats,
        tickets=tickets,
        search=search,
        category_filter=category_filter,
        priority_filter=priority_filter,
        status_filter=status_filter
    )


@app.route("/update-status/<int:ticket_id>", methods=["POST"])
def change_status(ticket_id):

    status = request.form.get("status", "")

    if update_ticket_status(ticket_id, status):
        flash("Ticket status updated successfully!", "success")
    else:
        flash("Invalid status or ticket not found.", "danger")

    return redirect(url_for("home") + "#tickets")


if __name__ == "__main__":
    app.run(debug=True)
