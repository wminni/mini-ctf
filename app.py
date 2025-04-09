from flask import Flask, request, render_template
import subprocess
import os

app = Flask(__name__)
REAL_FLAG = "flag{proud_of_you}"

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/challenge", methods=["GET", "POST"])
def challenge():
    output = ""
    show_flag_input = False
    correct_flag = False
    submitted_flag = request.form.get("flag")

    if request.method == "POST" and "host" in request.form:
        host = request.form["host"]
        try:
            output = subprocess.getoutput(f"ping -n 1 {host}")
            if "admin" in output:
                show_flag_input = True
        except Exception as e:
            output = str(e)

    if submitted_flag:
        correct_flag = submitted_flag.strip() == REAL_FLAG

    return render_template("index.html", output=output, show_flag_input=show_flag_input, correct_flag=correct_flag)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
