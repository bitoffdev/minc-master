import logging
import os

from pushjack import GCMClient

from minc import settings

client = GCMClient(api_key=settings.fcm_server_key)


def push_notification(registration_ids, title, body, icon, message):
    notification = {"title": title, "body": body, "icon": icon}
    alert = {"message": message, "notification": notification}

    # Send to single device.
    # NOTE: Keyword arguments are optional.
    res = client.send(
        registration_ids,
        alert,
        notification=notification,
        collapse_key="collapse_key",
        delay_while_idle=True,
        time_to_live=604800,
    )
    logger(res)


def logger(res):
    # List of requests.Response objects from GCM Server.
    # List of messages sent.
    # List of registration ids sent.
    # List of server response data from GCM.
    # List of successful registration ids.
    # List of failed registration ids.
    # List of exceptions.
    # List of canonical ids (registration ids that have changed).
    response_body = [
        "requests",
        "messages",
        "registration_ids",
        "data",
        "successes",
        "failures",
        "errors",
        "canonical_ids",
    ]
    for i in response_body:
        log_name = i + ".log"
        logfile = os.path.join(os.pardir, log_name)
        handler = logging.FileHandler(logfile)
        log = logging.getLogger()
        log.addHandler(handler)
        log.setLevel(logging.INFO)

        log.info(getattr(res, i, None))
