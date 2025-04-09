from flask import Flask, request, render_template, redirect, url_for, session
import os
import subprocess
import base64

app = Flask(__name__)
app.secret_key = "minictf_secret"

REAL_USERNAME = "admin"
REAL_PASSWORD = "' OR '1'='1"
REAL_FLAG = "flag{realistic_flow_completed}"
ENCODED_FLAG = base64.b64encode(REAL_FLAG.encode()).decode()

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if username == REAL_USERNAME and ("' OR '1'='1" in password or password == REAL_PASSWORD):
        session["user"] = "admin"
        return redirect(url_for("admin"))
    return render_template("login.html", error="Login failed")

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
