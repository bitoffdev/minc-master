from flask import Flask
from .tasks import add

app = Flask(__name__)


@app.route("/")
def hello():
    add.delay(5, 6)
    return "Hello, World!"


@app.route("/api/v1/hook", methods=("POST",))
def hook():
    return '{"status": "ok"}'
