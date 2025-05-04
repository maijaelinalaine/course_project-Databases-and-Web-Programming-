import sqlite3, secrets
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
import config, users, events
import db

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    try:
        all_events = events.get_events()
        return render_template("index.html", events=all_events)
    
    except Exception:
        session["user_id"] = None
        session["username"] = None
        db.create_tables()
        return "Virhe: tapahtumien haku epäonnistui"

@app.route("/signup", methods=["POST"])       
def signup():
    require_login()
    check_csrf()
    event_id = request.form["event_id"]

    event = events.get_event(event_id)
    if not event:
        abort(404 )
    user_id = session["user_id"]

    events.signup(event_id, user_id)
    if user_id in events.get_signups(event_id):
        abort(403)

    return redirect(f"/event/{event_id}")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    try:
        user = users.get_user(user_id)
        if not user:
            abort(404)
        events = users.get_events(user_id)
        if not events:
            events = []
        signups = users.get_signups(user_id)
        if not signups:
            signups = []

        return render_template("show_user.html", user=user, events=events, signups=signups)
    
    except Exception:
        return "Virhe: Käyttäjän näyttäminen epäonnistui"

@app.route("/search")
def search():
    try:
        query = request.args.get("query")
        if query:
            results = events.search(query)
        else:
            query = ""
            results = []
        return render_template("search.html", query=query, results=results)
    
    except Exception:
        return "Virhe: tapahtumien haku epäonnistui"
    
@app.route("/edit_event/<int:event_id>")
def edit_event(event_id):
    require_login()
    try:
        event = events.get_event(event_id)
        if not event:
            abort(404)
        if event["user_id"] != session["user_id"]:
            abort(403)
                
        event_types = events.get_event_types()

        return render_template("edit_event.html", event=event, event_types=event_types)
                               
    except Exception:
        return "Virhe: tapahtuman muokkaus epäonnistui"

@app.route("/edit_event/<int:event_id>", methods=["POST"])
def update_event(event_id):
    require_login()
    check_csrf()
    try:
        event = events.get_event(event_id)
        if not event:
            abort(404)
        if event["user_id"] != session["user_id"]:
            abort(403)
            
        title = request.form["title"]
        if not title or len(title) > 50:
            abort(403)
        
        event_time = request.form["event_time"]
        if not event_time:
            abort(403)

        description = request.form["description"]
        if not description or len(description) > 5000:
            abort(403)

        event_type = request.form["event_type"]
        if not event_type:
            abort(403)

        events.update_event(event_id, title, event_time, description, event_type)
        
        return redirect("/event/" + str(event_id))
    
    except Exception:
        return "Virhe: tapahtuman muokkaus epäonnistui"

@app.route("/remove/<int:event_id>", methods=["GET", "POST"])
def remove_event(event_id):
    require_login()
    try:
        event = events.get_event(event_id)
        if not event:
            abort(404)

        if request.method == "GET":
            return render_template("remove_event.html", event=event)
        
        if request.method == "POST":
            check_csrf()
            if "continue" in request.form:
                events.remove_event(event_id)
                return redirect("/")
            else:
                return redirect(f"/event/{event_id}")
        
    except Exception as e:
        return f"Virhe: tapahtuman poistaminen epäonnistui. {str(e)}"

@app.route("/event/<int:event_id>")
def show_event(event_id):
    try:
        event = events.get_event(event_id)
        if not event:
            abort(404)

        event_time = event["event_time"]
        event_type = event["event_type"]
        signups = events.get_signups(event_id)
        
        return render_template("show_event.html", event=event, event_time=event_time, event_type=event_type, signups=signups)
    
    except Exception:
        return "Virhe: tapahtuman näyttäminen epäonnistui"
    
@app.route("/new_event")
def new_event():
    require_login()

    event_types = events.get_event_types()

    return render_template("new_event.html", event_types=event_types)

@app.route("/create_event", methods=["POST"])
def create_event():
    require_login()
    check_csrf()
    try:
        event_time = request.form["event_time"]
        title = request.form["title"]
        if not title or len(title) > 50:
            abort(403)

        description = request.form["description"]
        if not description or len(description) > 5000:
            abort(403)

        event_type = request.form["event_type"]
        event_types = []
        if event_type:
            event_types.append(event_type)

        if not event_type:
            abort(403)
        
        if "user_id" not in session:
            return redirect("/login")
        user_id = session["user_id"]

        event_id = events.add_event(title, event_time, description, event_type, user_id)
        
        return redirect(f"/event/{event_id}")
        
    except ValueError:
        return redirect("/new_event")
    
    except Exception:
        return redirect("/new_event")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    return redirect("/")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        
        else:
            return "VIRHE: väärä tunnus tai salasana"
    
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

