from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta
import sqlite3
from pathlib import Path
from datetime import date, timedelta




DB_NAME = "nfl_subscriptions.db"


# --------------------- DB helpers ---------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # --- users table (for signup / login) ---
    c.execute("DROP TABLE IF EXISTS users")
    c.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    # --- subscriptions table ---

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

def create_user(username: str, email: str, password: str):
    conn = get_db_connection()
    c = conn.cursor()

    password_hash = generate_password_hash(password)
    created_at = date.today().isoformat()

    try:
        c.execute(
            "INSERT INTO users (username, email, password_hash, created_at) "
            "VALUES (?, ?, ?, ?)",
            (username, email, password_hash, created_at),
        )
        conn.commit()
        return True, "User created successfully."
    except sqlite3.IntegrityError:
        # username already exists
        return False, "Username already taken."
    finally:
        conn.close()


def verify_user(username: str, password: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "SELECT password_hash FROM users WHERE username=?",
        (username,),
    )
    row = c.fetchone()
    conn.close()

    if not row:
        return False

    password_hash = row[0]
    return check_password_hash(password_hash, password)


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

        # 🚫 1) Block if this team is already active for this user
        if self.has_active_subscription(username, team):
            conn.close()
            return (
                f"{username} already has an active subscription for {team}. "
                f"Please choose a different team."
            )

        # ✅ 2) Otherwise, we either renew an expired sub or create a new one
        expires_at = self._calculate_expiry(plan)

        # Look for an existing row for that exact (user, team)
        c.execute(
            "SELECT id FROM subscriptions WHERE username=? AND team=?",
            (username, team),
        )
        row = c.fetchone()

        if row:
            # Team exists but is NOT active (expired or manually deactivated)
            c.execute(
                "UPDATE subscriptions "
                "SET plan=?, active=1, expires_at=? "
                "WHERE id=?",
                (plan, expires_at, row[0]),
            )
            msg = (
                f"{username}'s subscription for {team} was renewed to {plan}, "
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
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})         
if not Path(DB_NAME).exists():
    init_db()

sms = SubscriptionManagementSystem()
cds = ContentDeliverySystem(sms)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username")
    email = data.get("email", "")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "status": "error",
            "message": "Missing 'username' or 'password'."
        }), 400

    ok, msg = create_user(username, email, password)
    status_code = 200 if ok else 400
    status = "ok" if ok else "error"
    return jsonify({"status": status, "message": msg}), status_code



@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "status": "error",
            "message": "Missing 'username' or 'password'."
        }), 400

    if verify_user(username, password):
        return jsonify({
            "status": "ok",
            "message": f"Login successful for {username}."
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid username or password."
        }), 401

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
def user_exists(username: str) -> bool:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT 1 FROM users WHERE username=?", (username,))
        row = c.fetchone()
        conn.close()
        return row is not None
@app.route("/checkout", methods=["POST"])
def checkout():
    """
    Frontend sends JSON: { username, plan, teams: [ {name, price}, ... ] }
    """
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username")
    teams = data.get("teams", [])
    plan = data.get("plan", "1_month")

    if not username or not teams:
        return jsonify({
            "status": "error",
            "message": "Missing 'username' or 'teams'."
        }), 400

    # ✅ verify that the user already exists
    if not user_exists(username):
        return jsonify({
            "status": "error",
            "message": f"User '{username}' not found. Please log in again."
        }), 400

    msgs = []
    for team in teams:
        team_name = team.get("name") if isinstance(team, dict) else str(team)
        if team_name:
            msg = sms.subscribe_team(username, team_name, plan)
            msgs.append(msg)

    return jsonify({
        "status": "ok",
        "message": "Checkout completed.",
        "details": msgs
    })


@app.route("/stream", methods=["POST"])
@app.route("/stream/<username>/<team>", methods=["GET"])
def stream(username=None, team=None):
    if request.method == "POST":
        data = request.get_json(force=True, silent=True) or {}
        username = data.get("username")
        team = data.get("team")
    else:
        # For GET requests, take from URL path
        if not username or not team:
            return (
                jsonify(
                    {"status": "error", "message": "Missing 'username' or 'team' parameter."}
                ),
                400,
            )

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

@app.route("/subscriptions_all", methods=["GET"])
def subscriptions_all():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, team, plan, active, expires_at FROM subscriptions")
    rows = c.fetchall()
    conn.close()

    data = [
        {
            "id": r[0],
            "username": r[1],
            "team": r[2],
            "plan": r[3],
            "active": bool(r[4]),
            "expires_at": r[5],
        }
        for r in rows
    ]

    return jsonify({"count": len(data), "subscriptions": data})

@app.route("/users_all", methods=["GET"])
def users_all():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, created_at FROM users")
    rows = c.fetchall()
    conn.close()

    data = [
        {
            "id": r[0],
            "username": r[1],
            "email": r[2],
            "created_at": r[3],
        }
        for r in rows
    ]

    return jsonify({"count": len(data), "users": data})

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "NFL Subscription API with expiry",
        "endpoints": ["/subscribe", "/unsubscribe", "/subscriptions_all", "/users_all"]
    })
@app.route("/profile/<username>", methods=["GET"])
def profile(username):
    conn = get_db_connection()
    c = conn.cursor()

    # --- get basic user info ---
    c.execute(
        "SELECT username, email, created_at FROM users WHERE username = ?",
        (username,),
    )
    user_row = c.fetchone()

    # --- get this user's active subscriptions ---
    c.execute(
        """
        SELECT team, plan, expires_at, active
        FROM subscriptions
        WHERE username = ?
        """,
        (username,),
    )
    subs_rows = c.fetchall()
    conn.close()

    if not user_row:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"User '{username}' not found.",
                }
            ),
            404,
        )

    user_info = {
        "username": user_row[0],
        "email": user_row[1],
        "created_at": user_row[2],
    }

    subs_list = []
    from datetime import date

    for team, plan, expires_at, active in subs_rows:
        try:
            exp_date = date.fromisoformat(expires_at)
            days_left = (exp_date - date.today()).days
        except Exception:
            days_left = None

        subs_list.append(
            {
                "team": team,
                "plan": plan,
                "expires_at": expires_at,
                "days_left": days_left,
                "active": bool(active),
            }
        )

    return jsonify(
        {
            "status": "ok",
            "user": user_info,
            "subscriptions": subs_list,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)