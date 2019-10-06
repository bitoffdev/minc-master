from flask import Flask, jsonify, request, render_template

from minc import tasks
from minc import model
from minc import redis

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/api/v1/hook", methods=("POST",))
def hook():
    # only accept JSON payloads
    json_payload = request.get_json(force=True)
    package_name = json_payload.get("packageName")
    op_package_name = json_payload.get("OpPackage")
    user_reg = json_payload.get("id")
    fcm_token = json_payload.get("fcmToken")
    post_time = json_payload.get("thread")

    # Please do not DOS our own servers
    redis_check = redis.check_thread(user_reg, fcm_token, post_time)
    if not redis_check and (
        package_name == "com.abotimable.minc"
        or op_package_name == "com.abotimable.minc"
    ):
        return jsonify({"status": "rejected"})

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
