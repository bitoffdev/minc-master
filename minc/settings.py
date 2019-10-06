import os

from dotenv import load_dotenv

# Read variables from the file `.env` if it exists and populate os.environ.
# This will not override system environmental variables.
load_dotenv()

# Load from the environment.
fcm_server_key = os.environ.get("FCM_SERVER_KEY")
