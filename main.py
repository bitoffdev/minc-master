"""
This is the one and only main program for the Minc backend.

Usage:
    python3 main.py --help
"""
import logging
logging.basicConfig(level=logging.INFO)

def elasticsearch():
    import logging
    from cmreslogging.handlers import CMRESHandler
    handler = CMRESHandler(hosts=[{'host': 'localhost', 'port': 9200}],
                           auth_type=CMRESHandler.AuthType.NO_AUTH,
                           es_index_name="minc_index")
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)


def www(args):
    """start a web server"""
    from minc.view import app

    app.run(host="0.0.0.0", port=5000)


def worker(args):
    """start a celery worker"""
    import celery.signals

    @celery.signals.setup_logging.connect
    def on_celery_setup_logging(**kwargs):
        pass


    # from celery import current_app
    from celery.bin import worker
    from minc.tasks import app

    # app = current_app._get_current_object()

    worker = worker.worker(app=app)

    options = {
        "broker": "amqp://guest:guest@localhost:5672//",
        "loglevel": args.loglevel,
        "traceback": True,
        "worker_hijack_root_logger": False,
    }

    worker.run(**options)


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog=__file__)
    parser.add_argument("--elasticsearch", action="store_true", default=False)
    subparsers = parser.add_subparsers(help="sub-command help")

    subparsers.add_parser("www", help="run the web server").set_defaults(func=www)

    worker_parser = subparsers.add_parser("worker", help="run a celery/rabbit worker")
    worker_parser.add_argument(
        "--loglevel",
        type=str,
        default="INFO",
        help="level of the logger",
        choices=["INFO", "ERROR", "DEBUG"],
    )
    worker_parser.set_defaults(func=worker)

    args = parser.parse_args(sys.argv[1:])

    if not "func" in args:
        parser.print_help()
        raise SystemExit
    if args.elasticsearch:
        elasticsearch()
    args.func(args)


if __name__ == "__main__":
    main()
