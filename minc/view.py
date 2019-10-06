from flask import Flask, request
from minc import tasks

app = Flask(__name__)


@app.route("/")
def hello():
    tasks.add.delay(5, 6)
    return "Hello, World!"


@app.route("/api/v1/hook", methods=("POST",))
def hook():
    # only accept JSON payloads
    json_payload = request.get_json(force=True)
    tasks.hook.delay(json_payload)
    return '{"status": "ok"}'
