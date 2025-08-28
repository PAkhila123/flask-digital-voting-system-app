from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey123"  # session management


# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # voters table
    cur.execute("""CREATE TABLE IF NOT EXISTS voters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    has_voted INTEGER DEFAULT 0)""")

    # candidates table
    cur.execute("""CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    votes INTEGER DEFAULT 0)""")

    # Insert default candidates (only once)
    cur.execute("SELECT * FROM candidates")
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO candidates (name) VALUES ('Alice')")
        cur.execute("INSERT INTO candidates (name) VALUES ('Bob')")
        cur.execute("INSERT INTO candidates (name) VALUES ('Charlie')")

    conn.commit()
    conn.close()


def get_db():
    return sqlite3.connect("database.db")


# initialize database on first run
init_db()


# ---------- Routes ----------
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # check if user exists
        cursor.execute("SELECT * FROM voters WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("Username already taken. Try another!", "danger")
            return redirect(url_for('register'))

        cursor.execute("INSERT INTO voters (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM voters WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):  # user[2] = password column
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('vote'))
        else:
            flash("Invalid username or password!", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'username' not in session:
        flash("Please login first!", "warning")
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # check if user has already voted
    cursor.execute("SELECT has_voted FROM voters WHERE username=?", (session['username'],))
    has_voted = cursor.fetchone()[0]

    if has_voted:
        flash("You have already voted!", "danger")
        conn.close()
        return redirect(url_for('results'))

    if request.method == 'POST':
        candidate_id = request.form['candidate']
        # increase candidate vote count
        cursor.execute("UPDATE candidates SET votes = votes + 1 WHERE id=?", (candidate_id,))
        # mark voter as voted
        cursor.execute("UPDATE voters SET has_voted=1 WHERE username=?", (session['username'],))
        conn.commit()
        conn.close()
        flash("Your vote has been submitted!", "success")
        return redirect(url_for('results'))

    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()
    conn.close()
    return render_template('vote.html', candidates=candidates)


@app.route('/results')
def results():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM candidates")
    candidates = cur.fetchall()
    conn.close()

    total_votes = sum([c[2] for c in candidates])  # sum of votes column
    return render_template("results.html", candidates=candidates, total_votes=total_votes)


@app.route("/results_data")
def results_data():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM candidates")
    candidates = cur.fetchall()
    conn.close()

    total_votes = sum([c[2] for c in candidates])

    results = []
    for c in candidates:
        results.append({
            "id": c[0],
            "name": c[1],
            "votes": c[2],
            "percentage": round((c[2] / total_votes * 100), 1) if total_votes > 0 else 0
        })

    return {"candidates": results, "total_votes": total_votes}


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)

