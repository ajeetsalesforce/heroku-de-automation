# subprocess_utils.py

import subprocess
import re

def run_command(command):
    """
    Function to run shell commands.
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode(), process.returncode

def get_connect_addons(app_name):
    """
    Function to get the Heroku Connect addons associated with a Heroku app.
    """
    command = f"heroku addons -a {app_name}"
    stdout, stderr, returncode = run_command(command)
    connect_addon_names = []  
    pattern = r'\((.*?)\)'
    if returncode == 0:
        lines = stdout.split('\n')
        for line in lines:
          if line.startswith('herokuconnect'):
             match = re.search(pattern, line)
             if match:
                 addon_resource_name  = match.group(1)
                 connect_addon_names.append(addon_resource_name)
        return connect_addon_names
    else:
        print(f"Failed to get Heroku Connect addons: {stderr}")
        return []

