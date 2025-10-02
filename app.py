from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os, json
from hashlib import sha256
from main import process_input


app = Flask(__name__)
app.secret_key = "supersecretkey"

# File to store users
USERS_FILE = "data/users.json"

# -------------------------
# Safe user loading function
# -------------------------
def load_users():
    # Ensure file exists
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

    # Ensure file is not empty
    if os.path.getsize(USERS_FILE) == 0:
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

    with open(USERS_FILE, "r") as f:
        return json.load(f)

# -------------------------
# Login route
# -------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        users = load_users()
        hashed = sha256(password.encode()).hexdigest()

        if username in users and users[username] == hashed:
            session["user"] = username
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="Incorrect username or password")

    return render_template("login.html")

# -------------------------
# Signup route
# -------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        confirm = request.form["confirm"].strip()

        users = load_users()

        if username in users:
            return render_template("signup.html", error="User already exists")
        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        hashed = sha256(password.encode()).hexdigest()
        users[username] = hashed
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

        # Create empty password file for this user
        open(f"data/{username}.dat", "wb").close()

        flash("Sign-up successful! Please log in.")
        return redirect("/")
    return render_template("signup.html")

# -------------------------
# Chat route
# -------------------------
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        data = request.get_json()
        user_input = data.get("message", "")
        response = process_input(user_input)
        return jsonify({"response": response})

    # GET request -> serve the chat UI
    return render_template("chat.html")

# -------------------------
# Logout route
# -------------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app.run(debug=True)
