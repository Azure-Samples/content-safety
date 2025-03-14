import os
import asyncio
from dotenv import load_dotenv

from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.aio import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData


load_dotenv()

IMAGEM_LIMPA = "./images/image_1.jpg"
IMAGEM_VIOLENTA = "./images/image_2.jpg"
IMAGEM_SEXUAL = "./images/image_3.jpg"


async def analyze_text(text_name: str, image_path: str):
    endpoint = os.environ["AZURE_CONTENTSAFETY_ENDPOINT"]
    subscription_key = os.environ["AZURE_CONTENTSAFETY_KEY"]

    async with ContentSafetyClient(endpoint, AzureKeyCredential(subscription_key)) as client:
        with open(image_path, "rb") as file:
            request = AnalyzeImageOptions(image=ImageData(content=file.read()))

        try:
            response = await client.analyze_image(request)
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
    asyncio.run(analyze_text("IMAGEM_LIMPA", IMAGEM_LIMPA))
    asyncio.run(analyze_text("IMAGEM_VIOLENTA", IMAGEM_VIOLENTA))
    asyncio.run(analyze_text("IMAGEM_SEXUAL", IMAGEM_SEXUAL))
