from celery import Celery
import logging

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
    logger.info("Processing payload {}".format(payload))  # TODO this bad security-wise
