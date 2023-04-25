from flask import Flask, render_template, request, redirect, send_file
from yaml import load
from yaml.loader import Loader
from copy import deepcopy

app = Flask(__name__)
data = load(open("default.yaml", "r"), Loader)

for k in data["channels"].keys():
    data["channels"][k]["posts"] = []

print(data)

def html(file, **kwargs):
    a = render_template("template.html", sn=data["servername"])
    b = render_template(file, **kwargs)
    c = """
    <p id="end">%!</p>
    <style>
        #end {
            position: fixed;
            top: calc(100% - 45px);
        }
    </style>
    """.replace("%!", data["undermsg"])
    return a + b + c

@app.route("/")
def index():
    return html("index.html")

@app.route("/sm")
def server_message():
    return send_file("sm.txt")

@app.route("/<chan>/")
def chan(chan):
    return html("chan.html",
    cn=data["channels"][chan]["name"],
    cd=data["channels"][chan]["desc"],
    cs=chan,
    )

@app.route("/<chan>/posts")
def cposts(chan):
    return data["channels"][chan]["posts"]

@app.route("/<chan>/new")
def cnew(chan):
    return html("new.html", cn=data["channels"][chan]["name"], cs=chan)

@app.route("/<chan>/add", methods=["POST"])
def cadd(chan):
    title = request.form["title"]
    content  = request.form["content"]
    data["channels"][chan]["posts"].append({
        "title": title,
        "content": content
    })
    return redirect(f"/{chan}/")

@app.route("/chans")
def chans():
    a = deepcopy(data["channels"])

    for i in a:
        a[i].pop("posts")

    return a

app.run(host="0.0.0.0", port=80)