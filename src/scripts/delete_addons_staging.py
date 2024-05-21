import subprocess
import json
import re
from config_utils import *
    
def delete_connect_addons(app_name, addon_names):
    """
    Function to delete multiple Heroku Connect addons.
    """
    for addon_name in addon_names:
        try:
            # Run the Heroku CLI command to delete the addon
            subprocess.run(['heroku', 'addons:destroy', addon_name, '-a', app_name, '--confirm', app_name], check=True)
            print(f"Addon {addon_name} deleted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error deleting addon {addon_name}: {e}")

# Replace 'YOUR_APP_NAME' with your actual Heroku app name
app_name = 'stark-meadow-29619'

# Fetch the Heroku Connect addons associated with the app
connect_addons = get_connect_addons(app_name)

if connect_addons:
    print("Heroku Connect addons to be deleted:")
    print(connect_addons)

    # Delete the Heroku Connect addons
    delete_connect_addons(app_name, connect_addons)
else:
    print("No Heroku Connect addons found.")
