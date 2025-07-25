from flask import Flask, request, redirect, make_response
import base64
import json
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    usernames = [
        "tofu_ninja",
        "potato_queen",
        "penguin_boi",
        "sneeze_master",
        "pickle_wizard",
        "spaghetti_agent",
        "keyboard_cat99",
        "cactus_juggler",
        "toilet_emperor",
        "duck_detective"
    ]
    
    passwords = [
        "ILike2Sneeze@Midnight",
        "Y0uSmellLikeToast!",
        "P@ssword123LOL",
        "FunkyMonkey42$",
        "DontTouchMyPickle9!",
        "C0ffeeSp1llsEverywhere",
        "DucksRuleTheWorld#1",
        "404BrainNotFound!",
        "Waffles>Everything",
        "Sleepy_Cactus88$"
    ]
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("DELETE FROM users")
    for i in range(len(usernames)):
        c.execute("INSERT INTO users VALUES (usernames[i], passwords[i]))
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
            return "Flag: flag{that_was_easy,_right?!?!?!}"
    except:
        pass
    return redirect("/flags")

@app.route('/flags')
def access_denied():
    return open("flags.html").read(), 403

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0')
