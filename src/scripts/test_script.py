import requests

# Define the API endpoint and the path to the config file
url = 'https://connect-3-virginia.heroku.com/api/v3/connections/69198c75-a124-443e-bed1-eba21fe82316/actions/import'
config_file_path = '/Users/ajeet.tripathi/Desktop/WorkProjects/heroku-dataengineering-automation/herokuconnect-silhouetted-79106_orgh.json'

# Define the headers
headers = {
    'Authorization': 'Bearer YOUR_HEROKU_API_KEY'
}

# Open the config file in binary mode and attach it to the form data
with open(config_file_path, 'rb') as config_file:
    files = {
        'config': config_file
    }

    # Make the POST request
    response = requests.post(url, headers=headers, files=files)

# Check the response
if response.status_code == 202:
    print('Configuration import request accepted. Monitor the Heroku dashboard for progress.')
else:
    print(f'Failed to import configuration. Status code: {response.status_code}')
    print(f'Response: {response.text}')
