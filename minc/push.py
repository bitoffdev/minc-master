import os
from pushjack import GCMClient
import logging

client = GCMClient(api_key=os.environ['GCM'])


def push_notification(registration_ids, title, body, icon, message):
    notification = {'title': title, 'body': body, 'icon': icon}
    alert = {'message': message, 'notification': notification}

    # Send to single device.
    # NOTE: Keyword arguments are optional.
    res = client.send(registration_ids,
                      alert,
                      notification=notification,
                      collapse_key='collapse_key',
                      delay_while_idle=True,
                      time_to_live=604800)
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
    response_body = ["requests", "messages", "registration_ids", "data",
                     "successes", "failures", "errors", "canonical_ids"]
    for i in response_body:
        log_name = i + ".log"
        logfile = os.path.join(os.pardir, log_name)
        logging.basicConfig(level=logging.DEBUG, filename=logfile, filemode="a+",
                            format="%(asctime)-15s %(levelname)-8s %(message)s")

        logging.info(getattr(res, i))
