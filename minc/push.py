import logging
import os

from pyfcm import FCMNotification

from minc import settings

logger = logging.getLogger(__name__)

push_service = FCMNotification(api_key=settings.fcm_server_key)

def push_notification(registration_ids, title, body, icon, message):
    for token in registration_ids:
        result = push_service.notify_single_device(registration_id=token, message_title=title, message_body=body)
        logger.info(result)


def log_result(res):
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
