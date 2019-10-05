# Minc Master

Server and task manager for the "More Important Notification Center"

## Usage

- Run RabbitMQ on the standard port on localhost
- Install the dependencies: `python3 -m pip install --user -r requirements.txt`
- Start the server on port 5000: `python3 main.py www`
- Start the Celery worker: `python3 main.py worker`
- Auto-reformat the code: `black main.py minc`
