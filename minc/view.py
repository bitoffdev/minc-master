from flask import Flask, jsonify, request, render_template

from minc import tasks
from minc import model

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/api/v1/hook", methods=("POST",))
def hook():
    # only accept JSON payloads
    json_payload = request.get_json(force=True)
    tasks.hook.delay(json_payload)
    return jsonify({"status": "ok"})


@app.route("/api/v1/register", methods=("POST",))
def register():
    json_payload = request.get_json(force=True)
    email = json_payload["email"]
    password = json_payload["password"]
    user = model.create_user(email, password)
    return jsonify(
        {"status": "ok", "email": user.email, "id": user.id, "token": user.token}
    )
