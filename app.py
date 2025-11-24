from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path
from datetime import date, timedelta

DB_NAME = "nfl_subscriptions.db"


# --------------------- DB helpers ---------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Always recreate the table so schema is correct
    c.execute("DROP TABLE IF EXISTS subscriptions")

    c.execute(
        """
        CREATE TABLE subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            team TEXT NOT NULL,        -- comma-separated team list
            plan TEXT NOT NULL,        -- e.g. '1_month' or '1_year'
            active INTEGER NOT NULL DEFAULT 1,
            expires_at TEXT NOT NULL   -- ISO date: YYYY-MM-DD
        )
        """
    )

    conn.commit()
    conn.close()


def get_db_connection():
    return sqlite3.connect(DB_NAME)


# --------------------- Core logic ---------------------
class SubscriptionManagementSystem:
    def _calculate_expiry(self, plan: str) -> str:
        if not plan:
            plan = "1_month"
        plan = plan.lower().strip()

        if plan in ("1_month", "1m"):
            days = 30
        elif plan in ("1_year", "1y"):
            days = 365
        else:
            try:
                days = int(plan)  # treat as X days
            except ValueError:
                days = 30

        return (date.today() + timedelta(days=days)).isoformat()

    def subscribe_team(self, username: str, team: str, plan: str = "1_month") -> str:
        conn = get_db_connection()
        c = conn.cursor()

        expires_at = self._calculate_expiry(plan)

        # Look for an existing row for that exact (user, team)
        c.execute(
            "SELECT id FROM subscriptions WHERE username=? AND team=?",
            (username, team),
        )
        row = c.fetchone()

        if row:
            # Update plan + expiry for THIS TEAM only
            c.execute(
                "UPDATE subscriptions "
                "SET plan=?, active=1, expires_at=? "
                "WHERE id=?",
                (plan, expires_at, row[0]),
            )
            msg = (
                f"{username}'s plan for {team} updated to {plan}, "
                f"expires {expires_at}."
            )
        else:
            # New team subscription for this user
            c.execute(
                "INSERT INTO subscriptions (username, team, plan, active, expires_at) "
                "VALUES (?, ?, ?, 1, ?)",
                (username, team, plan, expires_at),
            )
            msg = (
                f"{username} subscribed to {team} "
                f"(plan: {plan}, expires {expires_at})."
            )

        conn.commit()
        conn.close()
        return msg

    def list_subscription_info(self, username: str):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "SELECT team, plan, expires_at "
            "FROM subscriptions "
            "WHERE username=? AND active=1",
            (username,),
        )
        rows = c.fetchall()
        conn.close()

        if not rows:
            return None

        from datetime import date

        subscriptions = []
        for team, plan, expires_at in rows:
            try:
                exp_date = date.fromisoformat(expires_at)
                days_left = (exp_date - date.today()).days
            except Exception:
                days_left = None

            subscriptions.append(
                {
                    "team": team,
                    "plan": plan,
                    "expires_at": expires_at,
                    "days_left": days_left,
                }
            )

        return subscriptions
    
    def has_active_subscription(self, username: str, team: str) -> bool:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "SELECT plan, expires_at FROM subscriptions "
            "WHERE username=? AND team=? AND active=1",
            (username, team),
        )
        row = c.fetchone()
        conn.close()

        if not row:
            return False

        from datetime import date
        plan, expires_at = row
        try:
            exp_date = date.fromisoformat(expires_at)
            days_left = (exp_date - date.today()).days
        except Exception:
            return False

        return days_left >= 0


class ContentDeliverySystem:
    def __init__(self, subscription_manager: SubscriptionManagementSystem):
        self.subscription_manager = subscription_manager

    def deliver_content(self, username: str, team: str):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "SELECT plan, expires_at FROM subscriptions "
            "WHERE username=? AND team=?",
            (username, team),
        )
        row = c.fetchone()
        conn.close()

        if not row:
            return {
                "status": "error",
                "message": f"User '{username}' has no active subscription for '{team}'.",
            }

        plan, expires_at = row

        from datetime import date
        try:
            exp_date = date.fromisoformat(expires_at)
            days_left = (exp_date - date.today()).days
        except Exception:
            return {
                "status": "error",
                "message": "Subscription data is corrupted. Please contact support.",
            }

        if days_left < 0:
            return {
                "status": "error",
                "message": f"The subscription for '{team}' has expired. Please renew.",
            }

        return {
            "status": "ok",
            "message": f"Streaming content for '{team}' to user '{username}'.",
            "plan": plan,
            "expires_at": expires_at,
            "days_left": days_left,
        }

# --------------------- Flask app ---------------------
app = Flask(__name__)

if not Path(DB_NAME).exists():
    init_db()

sms = SubscriptionManagementSystem()
cds = ContentDeliverySystem(sms)


@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username")
    team = data.get("team")
    plan = data.get("plan", "1_month")  # "1_month" or "1_year" or custom days

    if not username or not team:
        return (
            jsonify(
                {"status": "error", "message": "Missing 'username' or 'team' field."}
            ),
            400,
        )

    msg = sms.subscribe_team(username, team, plan)
    return jsonify({"status": "ok", "message": msg})

@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    data = request.get_json()
    username = data.get("username")
    team = data.get("team")

    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        "DELETE FROM subscriptions WHERE username=? AND team=?",
        (username, team)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "message": f"{username} unsubscribed from {team}.",
        "status": "deleted"
    })

@app.route("/subscriptions/<username>", methods=["GET"])
def subscription_info(username):
    info = sms.list_subscription_info(username)
    if not info:
        return (
            jsonify(
                {
                    "username": username,
                    "has_subscription": False,
                    "message": "No active subscription found.",
                }
            ),
            404,
        )

    return jsonify(
        {
            "username": username,
            "has_subscription": True,
            "subscriptions": info,  # list of {team, plan, expires_at, days_left}
        }
    )


@app.route("/stream", methods=["POST"])
def stream():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username")
    team = data.get("team")

    if not username or not team:
        return (
            jsonify(
                {"status": "error", "message": "Missing 'username' or 'team' field."}
            ),
            400,
        )

    result = cds.deliver_content(username, team)
    status_code = 200 if result["status"] == "ok" else 403
    return jsonify(result), status_code


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running", "message": "NFL Subscription API with expiry"})


if __name__ == "__main__":
    app.run(debug=True)