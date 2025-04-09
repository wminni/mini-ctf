from flask import Flask, request, render_template, redirect, url_for, session
import os
import subprocess

app = Flask(__name__)
app.secret_key = "minictf_secret"

REAL_USERNAME = "admin"
REAL_PASSWORD = "' OR '1'='1"
REAL_FLAG = "flag{realistic_flow_completed}"

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
    flag_revealed = False

    if request.method == "POST":
        command = request.form.get("command", "")
        try:
            output = subprocess.getoutput(command)
            if "whoami" in command and "render" in output:
                flag_revealed = True
        except Exception as e:
            output = str(e)

    return render_template("admin.html", output=output, show_flag=flag_revealed)

@app.route("/flag")
def flag():
    if session.get("user") != "admin":
        return redirect(url_for("login"))
    return render_template("flag.html", flag=REAL_FLAG)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
