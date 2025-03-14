import os
import asyncio
from dotenv import load_dotenv

from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.aio import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions


load_dotenv()

TEXTO_LIMPO = """
Em uma pequena cidade, um homem chamado João decidiu abrir uma loja de doces.
Ele sempre teve uma paixão por doces e queria compartilhar essa paixão com a comunidade.
No entanto, João não tinha muito dinheiro, então ele começou a vender doces caseiros que ele mesmo fazia.
A loja de João rapidamente se tornou popular entre as crianças e os adultos da cidade.
Com o tempo, a loja de doces de João cresceu e se tornou uma das mais populares da cidade.
Um dia, ele decidiu abrir uma segunda loja em uma cidade vizinha.
Para isso, ele teve que trabalhar ainda mais duro.
Ele queria levar seus doces para mais pessoas e compartilhar sua história de sucesso.
Ele trabalhou duro para fazer isso acontecer e, eventualmente, conseguiu abrir a nova loja.
A nova loja de João também se tornou um sucesso, e ele ficou muito feliz em ver sua paixão pelos doces se espalhando.
Ele sempre acreditou que, com trabalho duro e dedicação, qualquer um pode alcançar seus sonhos.
A história de João é um exemplo inspirador de como seguir sua paixão pode levar ao sucesso.
Ele mostrou que, mesmo começando com pouco, é possível construir algo grande e significativo.
"""

TEXTO_COM_ODIO = """
Em uma pequena cidade, um homem chamado João decidiu abrir uma loja de doces.
Ele sempre teve uma paixão por doces e queria compartilhar essa paixão com a comunidade.
No entanto, João não tinha muito dinheiro, então ele começou a vender doces caseiros que ele mesmo fazia.
A loja de João rapidamente se tornou popular entre as crianças e os adultos da cidade, e os gordos desgraçados que não param de engordar.
Com o tempo, a loja de doces de João cresceu e se tornou uma das mais populares da cidade.
Um dia, ele decidiu abrir uma segunda loja em uma cidade vizinha.
Para isso, ele teve que trabalhar ainda mais duro.
Ele queria levar seus doces para mais pessoas e compartilhar sua história de sucesso.
Ele trabalhou duro para fazer isso acontecer e, eventualmente, conseguiu abrir a nova loja.
A nova loja de João também se tornou um sucesso, e ele ficou muito feliz em ver sua paixão pelos doces se espalhando.
Ele sempre acreditou que, com trabalho duro e dedicação, qualquer um pode alcançar seus sonhos.
A história de João é um exemplo inspirador de como seguir sua paixão pode levar ao sucesso.
Ele mostrou que, mesmo começando com pouco, é possível construir algo grande e significativo.
"""

TEXTO_COM_VIOLENCIA = """
Em uma pequena cidade, um homem chamado João decidiu abrir uma loja de doces.
Ele sempre teve uma paixão por doces e queria compartilhar essa paixão com a comunidade.
No entanto, João não tinha muito dinheiro, então ele começou a vender doces caseiros que ele mesmo fazia.
A loja de João rapidamente se tornou popular entre as crianças e os adultos da cidade.
Com o tempo, a loja de doces de João cresceu e se tornou uma das mais populares da cidade.
Um dia, ele decidiu abrir uma segunda loja em uma cidade vizinha.
Para isso, ele teve que trabalhar ainda mais duro, assassinando e estripando a tiros e facadas concorrentes potenciais.
Ele queria levar seus doces para mais pessoas e compartilhar sua história de sucesso, sem os malditos concorrentes.
Ele trabalhou duro para fazer isso acontecer e, eventualmente, conseguiu abrir a nova loja.
A nova loja de João também se tornou um sucesso, e ele ficou muito feliz em ver sua paixão pelos doces se espalhando.
Ele sempre acreditou que, com trabalho duro e dedicação, qualquer um pode alcançar seus sonhos.
A história de João é um exemplo inspirador de como seguir sua paixão pode levar ao sucesso.
Ele mostrou que, mesmo começando com pouco, é possível construir algo grande e significativo.
"""

TEXTO_COM_SEXUAL = """
Em uma pequena cidade, um homem chamado João decidiu abrir uma loja de doces.
Ele sempre teve uma paixão por doces e queria compartilhar essa paixão com a comunidade.
No entanto, João não tinha muito dinheiro, então ele começou a vender doces caseiros que ele mesmo fazia.
A loja de João rapidamente se tornou popular entre as crianças e os adultos da cidade, principalmente as prostitutas que faziam sexo oral em troca de doces.
Com o tempo, a loja de doces de João cresceu e se tornou uma das mais populares da cidade.
Um dia, ele decidiu abrir uma segunda loja em uma cidade vizinha.
Para isso, ele teve que trabalhar ainda mais duro.
Ele queria levar seus doces para mais pessoas e compartilhar sua história de sucesso.
Ele trabalhou duro para fazer isso acontecer e, eventualmente, conseguiu abrir a nova loja.
A nova loja de João também se tornou um sucesso, e ele ficou muito feliz em ver sua paixão pelos doces se espalhando.
Ele sempre acreditou que, com trabalho duro e dedicação, qualquer um pode alcançar seus sonhos.
A história de João é um exemplo inspirador de como seguir sua paixão pode levar ao sucesso.
Ele mostrou que, mesmo começando com pouco, é possível construir algo grande e significativo.
"""

TEXTO_COM_SELF_HARM = """
Em uma pequena cidade, um homem chamado João decidiu abrir uma loja de doces.
Ele sempre teve uma paixão por doces e queria compartilhar essa paixão com a comunidade.
No entanto, João não tinha muito dinheiro, então ele começou a vender doces caseiros que ele mesmo fazia.
A loja de João rapidamente se tornou popular entre as crianças e os adultos da cidade.
Com o tempo, a loja de doces de João cresceu e se tornou uma das mais populares da cidade.
Um dia, ele decidiu abrir uma segunda loja em uma cidade vizinha.
Para isso, ele teve que trabalhar ainda mais duro.
Ele queria levar seus doces para mais pessoas e compartilhar sua história de sucesso.
Ele trabalhou duro para fazer isso acontecer e, eventualmente, conseguiu abrir a nova loja.
A nova loja de João também se tornou um sucesso, e ele ficou muito feliz em ver sua paixão pelos doces se espalhando.
Ele sempre acreditou que, com trabalho duro e dedicação, qualquer um pode alcançar seus sonhos.
Ainda assim, ele acabou se suicidando por conta de sua vida sexual promíscua.
A história de João é um exemplo inspirador de como seguir sua paixão pode levar ao sucesso.
Ele mostrou que, mesmo começando com pouco, é possível construir algo grande e significativo.
"""


async def analyze_text(text_name: str, text: str):
    endpoint = os.environ["AZURE_CONTENTSAFETY_ENDPOINT"]
    subscription_key = os.environ["AZURE_CONTENTSAFETY_KEY"]

    async with ContentSafetyClient(endpoint, AzureKeyCredential(subscription_key)) as client:
        request = AnalyzeTextOptions(text=text)

        try:
            response = await client.analyze_text(request)
        except HttpResponseError as e:
            print("Analyze text failed.")
            if e.error:
                print(f"Error code: {e.error.code}")
                print(f"Error message: {e.error.message}")
                raise
            print(e)
            raise

    print(f"Texto do tipo {text_name}: \n", response.as_dict())


if __name__ == "__main__":
    asyncio.run(analyze_text("TEXTO_LIMPO", TEXTO_LIMPO))
    asyncio.run(analyze_text("TEXTO_COM_VIOLENCIA", TEXTO_COM_VIOLENCIA))
    asyncio.run(analyze_text("TEXTO_COM_ODIO", TEXTO_COM_ODIO))
    asyncio.run(analyze_text("TEXTO_COM_SEXUAL", TEXTO_COM_SEXUAL))
    asyncio.run(analyze_text("TEXTO_COM_SELF_HARM", TEXTO_COM_SELF_HARM))
