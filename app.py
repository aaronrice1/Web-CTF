from flask import Flask, request, redirect, make_response
import base64
import json
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("DELETE FROM users")
    c.execute("INSERT INTO users VALUES ('admin', 'supersecret')")
    c.execute("INSERT INTO users VALUES ('hacker', '1234')")
    conn.commit()
    conn.close()

@app.route('/')
@app.route('/login-roulette/')
def login():
    return open("login.html").read()

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    c.execute(query)
    result = c.fetchone()
    conn.close()
    if result:
        session_data = {"user": result[0], "role": "user"}
        session_str = base64.b64encode(json.dumps(session_data).encode()).decode()
        resp = make_response(redirect("/admin/flag"))
        resp.set_cookie("session", session_str)
        return resp
    return "Invalid credentials", 403

@app.route('/admin/flag')
def admin_flag():
    session_cookie = request.cookies.get("session", "")
    try:
        session_json = json.loads(base64.b64decode(session_cookie))
        if session_json.get("role") == "admin":
            return "Flag: CTF{sql_and_cookies_are_not_a_safe_dessert}"
    except:
        pass
    return "Access denied", 403

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0')
