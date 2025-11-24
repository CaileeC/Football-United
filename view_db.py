import sqlite3

# Connect to your database file
conn = sqlite3.connect("nfl_subscriptions.db")
c = conn.cursor()

# See what tables exist
print("Tables:")
for t in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print(" -", t[0])

# Show all subscriptions
print("\n--- Subscriptions Table ---")
for row in c.execute("SELECT * FROM subscriptions;"):
    print(row)

conn.close()