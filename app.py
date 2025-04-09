from flask import Flask, request, render_template, redirect, url_for, session
import os
import subprocess
import base64
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "minictf_secret"

REAL_USERNAME = "admin"
REAL_PASSWORD = "' OR '1'='1"
REAL_FLAG = "flag{nicely_done}"
ENCODED_FLAG = base64.b64encode(REAL_FLAG.encode()).decode()

MAX_ATTEMPTS = 50
LOCKOUT_TIME = timedelta(minutes=10)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if "login_attempts" not in session:
        session["login_attempts"] = 0
        session["first_attempt"] = datetime.utcnow().isoformat()

    first_time = datetime.fromisoformat(session["first_attempt"])
    if session["login_attempts"] >= MAX_ATTEMPTS:
        if datetime.utcnow() - first_time < LOCKOUT_TIME:
            return render_template("login.html", error="Too many login attempts detected. To protect against automated abuse (as required by the hosting platform), further attempts are temporarily disabled. Please try again after 10 minutes.")
        else:
            session["login_attempts"] = 0
            session["first_attempt"] = datetime.utcnow().isoformat()

    if username == REAL_USERNAME and ("' OR '1'='1" in password or password == REAL_PASSWORD):
        session["user"] = "admin"
        session.pop("login_attempts", None)
        session.pop("first_attempt", None)
        return redirect(url_for("admin"))

    session["login_attempts"] += 1
    return render_template("login.html", error="Login failed.")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if session.get("user") != "admin":
        return redirect(url_for("login"))

    output = ""
    show_flag_input = False
    correct_flag = False
    submitted_flag = request.form.get("flag")

    if request.method == "POST" and "command" in request.form:
        command = request.form.get("command", "")
        try:
            if "whoami" in command:
                output = ENCODED_FLAG
                show_flag_input = True
            else:
                output = "[Command executed]"
        except Exception as e:
            output = str(e)

    if submitted_flag:
        correct_flag = submitted_flag.strip() == REAL_FLAG

    return render_template("admin.html", output=output, show_flag_input=show_flag_input, correct_flag=correct_flag)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
