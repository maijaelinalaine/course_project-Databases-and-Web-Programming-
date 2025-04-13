import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import events

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    try:
        all_events = events.get_events()
        return render_template("index.html", events=all_events)
    except Exception:
        return f"Virhe: tapahtumien haku epäonnistui"
        
@app.route("/search")
def search():
    try:
        query = request.args.get("query")
        results = events.search_events(query) if query else []
        return render_template("search.html", query=query, results=results)
    except Exception:
        return f"Virhe: tapahtumien haku epäonnistui"
    
@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    try:
        event = events.get_event(event_id)

        if request.method == "GET":
            return render_template("edit_event.html", event=event)
        
        if request.method == "POST":
            description = request.form["description"]
            events.update_event(event["id"], description)

            return redirect("/event/" + str(event_id))
    except Exception:
        return f"Virhe: tapahtuman muokkaus epäonnistui"
    
@app.route("/remove/<int:event_id>", methods=["GET", "POST"])
def remove_event(event_id):
    try:
        event = events.get_event(event_id)

        if request.method == "GET":
            return render_template("remove.html", event=event)
        
        if request.method == "POST":
            if "continue" in request.form:
                events.remove_event(event["id"])
            return redirect("/event/" + str(event_id))
    except Exception:
        return f"Virhe: tapahtuman poistaminen epäonnistui"
    
@app.route("/event/<int:event_id>")
def show_event(event_id):
    try:
        event = events.get_event(event_id)
        if not event:
            return "VIRHE: tapahtumaa ei löydy"
        return render_template("show_event.html", event=event)
    except Exception:
        return f"Virhe: tapahtuman näyttäminen epäonnistui"
    
@app.route("/new_event")
def new_event():
    return render_template("new_event.html")

@app.route("/create_event", methods=["POST"])
def create_event():
    try:
        title = request.form["title"]
        description = request.form["description"]
        event_type = request.form["event_type"]
        if "user_id" not in session:
            return redirect("/login")
        user_id = session["user_id"]
        if not title or len(title) > 100 or len(description) > 1000:
            return "VIRHE: virheellinen tapahtuma"
        
        events.add_event(title, description, event_type, user_id)
        return redirect("/")
    except Exception:
        return f"Virhe: tapahtuman luominen epäonnistui"
    
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    try:
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return "VIRHE: salasanat eivät ole samat"
        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
        except sqlite3.IntegrityError:
            return "VIRHE: tunnus on jo varattu"

        return "Tunnus luotu"
    except Exception:
        return f"Virhe: tunnuksen luominen epäonnistui"

@app.route("/login", methods=["GET","POST"])
def login():
    try:
        if request.method == "GET":
            return render_template("login.html")

        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            sql = "SELECT id, password_hash FROM users WHERE username = ?"
            result = db.query(sql, [username])[0]
            user_id = result["id"]
            password_hash = result["password_hash"]

            if check_password_hash(password_hash, password):
                session["user_id"] = user_id
                session["username"] = username
                return redirect("/")
            else:
                return "VIRHE: väärä tunnus tai salasana"
    except Exception:
        return f"Virhe: kirjautuminen epäonnistui"
    
@app.route("/logout")
def logout():
    try:
        del session["user_id"]
        del session["username"]
        return redirect("/")
    except Exception:
        return f"Virhe: uloskirjautuminen epäonnistui"
    
if __name__ == "__main__":
    app.run(debug=True)
    db.create_tables()
