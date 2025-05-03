import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM events")
db.execute("DELETE FROM signups")

user_count = 1000
event_count = 10**5
signup_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, event_count + 1):
    db.execute("INSERT INTO events (title) VALUES (?)",
               ["event" + str(i)])

for i in range(1, signup_count + 1):
    user_id = random.randint(1, user_count)
    event_id = random.randint(1, event_count)
    db.execute("""INSERT INTO signups (user_id, event_id, signup_time)
                VALUES (?, ?, datetime('now'))""",
               ["signup" + str(i), user_id, event_id])

db.commit()
db.close()