
import sqlite3

DATABASE_NAME = "tickets.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_name TEXT NOT NULL,
                email TEXT NOT NULL,
                department TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT,
                severity TEXT,
                business_impact TEXT,
                priority TEXT,
                confidence REAL,
                status TEXT DEFAULT 'Open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    print("Database table created successfully!")


def insert_ticket(
    employee_name, email, department, title, description,
    category, severity, business_impact, priority, confidence
):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO tickets (
                employee_name, email, department, title, description,
                category, severity, business_impact, priority, confidence
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            employee_name, email, department, title, description,
            category, severity, business_impact, priority, confidence
        ))


def get_all_tickets(search="", category="", priority="", status=""):
    query = "SELECT * FROM tickets WHERE 1=1"
    parameters = []

    if search:
        query += """
            AND (
                CAST(ticket_id AS TEXT) LIKE ?
                OR employee_name LIKE ?
                OR title LIKE ?
                OR email LIKE ?
            )
        """
        value = f"%{search}%"
        parameters.extend([value, value, value, value])

    if category:
        query += " AND category = ?"
        parameters.append(category)

    if priority:
        query += " AND priority = ?"
        parameters.append(priority)

    if status:
        query += " AND status = ?"
        parameters.append(status)

    query += " ORDER BY ticket_id DESC"

    with get_connection() as connection:
        return connection.execute(query, parameters).fetchall()


def get_dashboard_stats():
    with get_connection() as connection:
        total = connection.execute(
            "SELECT COUNT(*) FROM tickets"
        ).fetchone()[0]

        open_count = connection.execute(
            "SELECT COUNT(*) FROM tickets WHERE status = 'Open'"
        ).fetchone()[0]

        progress_count = connection.execute(
            "SELECT COUNT(*) FROM tickets WHERE status = 'In Progress'"
        ).fetchone()[0]

        resolved_count = connection.execute(
            "SELECT COUNT(*) FROM tickets WHERE status = 'Resolved'"
        ).fetchone()[0]

        critical_count = connection.execute(
            "SELECT COUNT(*) FROM tickets WHERE severity = 'Critical'"
        ).fetchone()[0]

        high_priority_count = connection.execute(
            "SELECT COUNT(*) FROM tickets WHERE priority = 'P1'"
        ).fetchone()[0]

        category_data = connection.execute("""
            SELECT category, COUNT(*) AS count
            FROM tickets
            GROUP BY category
            ORDER BY count DESC
        """).fetchall()

        priority_data = connection.execute("""
            SELECT priority, COUNT(*) AS count
            FROM tickets
            GROUP BY priority
            ORDER BY priority
        """).fetchall()

    return {
        "total": total,
        "open": open_count,
        "in_progress": progress_count,
        "resolved": resolved_count,
        "critical": critical_count,
        "p1": high_priority_count,
        "categories": [dict(row) for row in category_data],
        "priorities": [dict(row) for row in priority_data]
    }


def update_ticket_status(ticket_id, status):
    allowed_statuses = ["Open", "In Progress", "Resolved"]

    if status not in allowed_statuses:
        return False

    with get_connection() as connection:
        cursor = connection.execute("""
            UPDATE tickets
            SET status = ?
            WHERE ticket_id = ?
        """, (status, ticket_id))

        return cursor.rowcount > 0


if __name__ == "__main__":
    create_table()
