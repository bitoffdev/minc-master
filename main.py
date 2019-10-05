"""
This is the one and only main program for the Minc backend.

Usage:
    python3 main.py --help
"""


def www(args):
    """start a web server"""
    from minc.view import app

    app.run(host="0.0.0.0", port=5000)


def worker(args):
    """start a celery worker"""
    # from celery import current_app
    from celery.bin import worker
    from minc.tasks import app

    # app = current_app._get_current_object()

    worker = worker.worker(app=app)

    options = {
        "broker": "amqp://guest:guest@localhost:5672//",
        "loglevel": args.loglevel,
        "traceback": True,
    }

    worker.run(**options)


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog=__file__)
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
    args.func(args)


if __name__ == "__main__":
    main()
