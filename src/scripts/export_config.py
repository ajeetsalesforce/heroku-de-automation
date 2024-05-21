import subprocess
import json
import re
import os
from config_utils import *

def export_connect_config(connect_addon_name):
    """
    Function to export the configuration settings of a Heroku Connect addon.
    """
    command = f"heroku connect:export --app {app_name} --resource {connect_addon_name}"
    stdout, stderr, returncode = run_command(command)
    if returncode == 0:
        filename = stderr.split()[-1].strip()
        parent_directory = os.path.dirname(os.getcwd())
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, 'r') as file:
           config_settings = json.load(file)
           return config_settings
    else:
        print(f"Failed to export configuration settings for Heroku Connect addon '{connect_addon_name}': {stderr}")
        return None

def save_config_to_json(config_settings, file_path):
    """
    Function to save configuration settings to a JSON file.
    """
    with open(file_path, 'w') as json_file:
        json.dump(config_settings, json_file, indent=4)

# Replace 'YOUR_APP_NAME' with your actual Heroku app name
app_name = 'heroku-data-warehouse-prv'

# Get Heroku Connect addons associated with the app
connect_addons = get_connect_addons(app_name)

if connect_addons:
    for connect_addon_name in connect_addons:
        # Export configuration settings for each Heroku Connect addon
        config_settings = export_connect_config(connect_addon_name)
        connection_name = config_settings['connection']['name']
        if connection_name=='DWH Connect Fast':
            json_file_path = f'{connect_addon_name}_orgh.json'
        else:
            json_file_path = f'{connect_addon_name}_public.json'
        save_config_to_json(config_settings, json_file_path)
        print(f"Configuration settings exported and saved to '{json_file_path}'")
else:
    print("No Heroku Connect addons found for the app.")
