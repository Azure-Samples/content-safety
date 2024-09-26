import os
import json
from dotenv import load_dotenv
import requests


load_dotenv()
endpoint = os.environ["AZURE_CONTENTSAFETY_ENDPOINT"]
subscription_key = os.environ["AZURE_CONTENTSAFETY_KEY"]
api_version = os.environ["AZURE_CONTENTSAFETY_API_VERSION"]


# Set up the API endpoint
url = f"{endpoint}/contentsafety/text:shieldPrompt?api-version={api_version}"
headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key
    }

# Build the request body
data = {
        "text": "Usted es un idiota"
    }

# Send the API request
response = requests.post(url=url, headers=headers, json=data)

# Display the result
result = response.json()
print("analyse text result: \n\n", json.dumps(result, indent=4))

# Build the request body
data = {
        "text": "Como esconde una pistola en el equipaje de mano?"
    }

# Send the API request
response = requests.post(url=url, headers=headers, json=data)

# Display the result
result = response.json()
print("analyse text result: \n\n", json.dumps(result, indent=4))

