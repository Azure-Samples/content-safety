import os
import json
from dotenv import load_dotenv
import requests


load_dotenv()
endpoint = os.environ["AZURE_CONTENTSAFETY_ENDPOINT"]
subscription_key = os.environ["AZURE_CONTENTSAFETY_KEY"]
api_version = os.environ["AZURE_CONTENTSAFETY_API_VERSION"]


url = f"{endpoint}/contentsafety/text:detectGroundedness?api-version={api_version}"
headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key
    }

# Body of the request
grounding_sources = """
Tengo 21 años y necesito tomar una decisión sobre los próximos dos años de mi vida.
Dentro de una semana. Actualmente, trabajo en un banco que exige metas de ventas rigurosas.
Si no se cumplen tres veces (tres meses), te despiden.
Me pagan 10 dólares por hora y no es raro recibir un aumento en unos 6 meses.
El problema es que no soy un vendedor.
Eso no forma parte de mi personalidad.
Soy excelente en la atención al cliente, tengo los informes más positivos de atención al cliente hechos sobre mí en el corto período en que he trabajado aquí.
Un compañero de trabajo preguntó: "¿Pides a las personas que llenen estos informes? Tienes muchos".
Dicho esto, tengo una oportunidad de trabajo en el Chase Bank como cajero a medio tiempo.
Lo que hace que esta decisión sea tan difícil es que, en mi trabajo actual, trabajo 40 horas, y en Chase solo podrían ofrecerme 20 horas por semana.
El tiempo de desplazamiento a mi trabajo actual también es de 21 millas solo de ida, mientras que Chase está literalmente a 1,8 millas de mi casa, permitiéndome ir a casa a almorzar.
Tengo un apartamento y un compañero de cuarto increíble que sé que no se retrasará con su parte del alquiler, así que pagar las cuentas con 20 horas por semana no es el problema.
El problema es el dinero extra y estar siempre sin dinero.
Anteriormente trabajé en Wal-Mart y llevaba a casa unos 400 dólares cada dos semanas.
Así que sé que puedo sobrevivir con ese ingreso.
Solo no sé si debo ir a Chase, ya que definitivamente me veo teniendo una carrera allí.
Soy estudiante de matemáticas y probablemente me convertiré en actuario, por lo que Chase podría brindarme excelentes oportunidades eventualmente.
""" 

query = "Cuanto recibe por hora actualmente en el banco?"

content_text = "12/hora."   # ungrounded answer

data = {
        "domain": "Generic",
        "task": "QnA",
        "text": content_text,
        "groundingSources": [grounding_sources],
        "qna": {"query": query},
        "reasoning": True , 
        "llmResource":{
            "resourceType": "AzureOpenAI",
            "azureOpenAIEndpoint":os.environ["AZURE_OPENAI_ENDPOINT"],
            "azureOpenAIDeploymentName": os.environ["AZURE_OPENAI_DEPLOYMENT_ID"]
        }
}


 # Send the API request
response = requests.post(url, headers=headers, json=data)

# Groundedness result
result = response.json()
print("Groundedness detection: \n\n", json.dumps(result, indent=4, ensure_ascii=False))

content_text = "10/hour."  # correct answer

data = {
        "domain": "Generic",
        "task": "QnA",
        "text": content_text,
        "groundingSources": [grounding_sources],
        "qna": {"query": query},
        "reasoning": True , 
        "llmResource":{
            "resourceType": "AzureOpenAI",
            "azureOpenAIEndpoint":os.environ["AZURE_OPENAI_ENDPOINT"],
            "azureOpenAIDeploymentName": os.environ["AZURE_OPENAI_DEPLOYMENT_ID"]
        }
}

 # Send the API request
response = requests.post(url, headers=headers, json=data)

# Groundedness result
result = response.json()
print("Groundedness detection: \n\n", json.dumps(result, indent=4))

