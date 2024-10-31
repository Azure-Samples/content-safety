import os
import json
from dotenv import load_dotenv
import requests


load_dotenv()
endpoint = os.environ["AZURE_CONTENTSAFETY_ENDPOINT"]
subscription_key = os.environ["AZURE_CONTENTSAFETY_KEY"]
api_version = os.environ["AZURE_CONTENTSAFETY_API_VERSION"]


# Set up the API endpoint
blocklistName = "TestBlocklist"
url = f"{endpoint}/contentsafety/text/blocklists/{blocklistName}?api-version={api_version}"	
headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key
    }


# Body of the request
data = {
  "description": "Test Blocklist"
}

# Send the API request
response = requests.patch(url=url, headers=headers, json=data)

# Display the result
result = response.json()
print("blocklist creation result: \n\n", json.dumps(result, indent=4))


url = f"{endpoint}/contentsafety/text/blocklists/{blocklistName}:addOrUpdateBlocklistItems?api-version={api_version}"	


# Create blocklist items
data = {
   "blocklistItems": [
       {
           "description": "violencia",
           "text": "sangrar"
       },
       {
           "description": "violencia",
           "text": "sangre"
       },
       {
           "description": "violencia",
           "text": "pistola"
       },
       {
           "description": "violencia",
           "text": "arma"
       }
   ]
}


# Send the API request
response = requests.post(url=url, headers=headers, json=data)

# Display the result
result = response.json()
print("blocklist creation result: \n\n", json.dumps(result, indent=4, ensure_ascii=False))


url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}&"

data = {
  "text": "Te voy a golpear hasta sangrar , y despues te voy a disparar con una arma",
  "categories": [
    "Hate",
    "Sexual",
    "SelfHarm",
    "Violence"
  ],
  "blocklistNames":[blocklistName],
  "haltOnBlocklistHit": False,
  "outputType": "FourSeverityLevels"
}


# Send the API request
response = requests.post(url=url, headers=headers, json=data)

# Display the result
result = response.json()
print("blocklist detection: \n\n", json.dumps(result, indent=4))


