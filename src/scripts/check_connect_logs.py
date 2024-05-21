# check_connect_logs.py

import subprocess
from config_utils import *


def check_connect_logs(app_name):
    """
    Function to check Connect logs for the specified Heroku app.
    """
    command = f"heroku logs --app {app_name} -d herokuconnect"
    print("Checking Connect logs...")
    stdout, stderr, returncode = run_command(command)
    if returncode != 0:
        print(f"Failed to check Connect logs: {stderr}")
    else:
        print(stdout)

# Replace 'YOUR_APP_NAME' with your actual Heroku app name
app_name = 'heroku-data-warehouse-prv'

# Check Connect logs
check_connect_logs(app_name)

