# automate_setup.py

import subprocess
import time
import json
from config_utils import *

def automate_setup(app_name):
    """
    Function to automate the setup process for Heroku Connect.
    """
    # Step 1: Check and rename schemas if needed
    command_org_check = f"heroku pg:psql -a {app_name} -c \"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = 'org' LIMIT 1);\""
    stdout, stderr, returncode = run_command(command_org_check)
    if returncode == 0 and 't' in stdout.strip():
        # Schema 'org' exists and contains tables, rename it
        command_org_rename = f"heroku pg:psql -a {app_name} -c \"ALTER SCHEMA org RENAME TO org_;\""
        run_command(command_org_rename)
        print("Schema 'org' renamed to 'org_'.")
    
    command_public_check = f"heroku pg:psql -a {app_name} -c \"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' LIMIT 1);\""
    stdout, stderr, returncode = run_command(command_public_check)
    if returncode == 0 and 't' in stdout.strip():
        # Schema 'public' exists and contains tables, rename it
        command_public_rename = f"heroku pg:psql -a {app_name} -c \"ALTER SCHEMA public RENAME TO public_;\""
        run_command(command_public_rename)
        print("Schema 'public' renamed to 'public_'.")
    
    # Step 2: Create new Heroku Connect addons
    command_connect_fast = f"heroku addons:create herokuconnect:fast -a {app_name}"
    stdout, stderr, returncode = run_command(command_connect_fast)
    if returncode == 0:
        print("Heroku Connect Fast addon created successfully.")
    else:
        print("Failed to create Heroku Connect Fast addon.")
        print(stderr)
    
    command_connect_cloud = f"heroku addons:create herokuconnect:cloud -a {app_name}"
    stdout, stderr, returncode = run_command(command_connect_cloud)
    if returncode == 0:
        print("Heroku Connect Cloud (Enterprise) addon created successfully.")
    else:
        print("Failed to create Heroku Connect Cloud (Enterprise) addon.")
        print(stderr)

    # Step 3: Wait for addons to be provisioned
    print("Waiting for addons to be provisioned...")
    time.sleep(60)  # Wait for 1 minute
    
    # Step 4: Check status of addons
    command_addons_info = f"heroku addons --json -a {app_name}"
    stdout, stderr, returncode = run_command(command_addons_info)
    if returncode == 0:
        addons_info = json.loads(stdout)
        for addon in addons_info:
            addon_name = addon['name']
            addon_status = addon['state']
            print(f"Addon '{addon_name}' status: {addon_status}")
    else:
        print(f"Failed to retrieve addons information: {stderr}")

# Replace 'YOUR_APP_NAME' with your actual Heroku app name
app_name = 'data-warehouse-staging'

# Automate the setup process
automate_setup(app_name)

