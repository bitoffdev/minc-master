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
    logging.basicConfig(level=logging.DEBUG, filename="requests", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(res.responses)

    # List of messages sent.
    logging.basicConfig(level=logging.DEBUG, filename="messages", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(res.messages)

    # List of registration ids sent.
    logging.basicConfig(level=logging.DEBUG, filename="registration_ids", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(res.registration_ids)

    # List of server response data from GCM.
    logging.basicConfig(level=logging.DEBUG, filename="response_data", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(res.data)

    # List of successful registration ids.
    logging.basicConfig(level=logging.DEBUG, filename="successes", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(res.successes)

    # List of failed registration ids.
    logging.basicConfig(level=logging.DEBUG, filename="\failures", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(res.failures)

    # List of exceptions.
    logging.basicConfig(level=logging.DEBUG, filename="errors", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(res.errors)

    # List of canonical ids (registration ids that have changed).
    logging.basicConfig(level=logging.DEBUG, filename="canonical_ids", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(res.canonical_ids)