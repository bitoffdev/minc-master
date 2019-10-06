import logging

from celery import Celery

from minc.push import push_notification

logger = logging.getLogger("minc.tasks")

app = Celery("tasks", broker="pyamqp://guest@localhost//")


@app.task
def add(x, y):
    logger.info("Adding together {} and {}".format(x, y))
    return x + y


@app.task
def hook(payload):
    # type: (dict) -> None
    """take a JSON payload and process it"""
    logger.info("Processing payload {}".format(payload))

    fcm_token = payload["fcmToken"]
    icon = payload["extras"].get("android.icon", None)
    title = payload["extras"].get("android.title", "Message")
    body = payload["extras"].get("android.text", "")
    message = payload["extras"].get("android.extraText", "")
    push_notification([fcm_token], title, body, icon, message)
