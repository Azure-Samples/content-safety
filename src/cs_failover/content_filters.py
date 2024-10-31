from typing import Self
from enum import Enum

import os
import logging
import dotenv
import requests

from azure.ai.contentsafety import ContentSafetyClient, BlocklistClient
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, AddOrUpdateTextBlocklistItemsOptions, TextBlocklistItem


dotenv.load_dotenv(dotenv.find_dotenv())
CS_KEY = os.getenv("AZURE_CONTENTSAFETY_KEY")
PHI_URL = os.getenv("PHI3_MINI_URL")
PHI_KEY = os.getenv("PHI3_MINI_KEY")
DEFAULT_CREDENTIAL = DefaultAzureCredential()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Level(Enum):
    LOW = 6
    MEDIUM = 4
    HIGH = 2


class ContentFilterFactory:

    def __init__(self, endpoint: str, level: Level):
        """
        Initializes the ContentFilters class with the given endpoint.
        Args:
            endpoint (str): The endpoint URL for the Content Safety Client.
        """
        self.client = ContentSafetyClient(endpoint, DEFAULT_CREDENTIAL)
        self.blocklist = BlocklistClient(endpoint, DEFAULT_CREDENTIAL)
        self.level = level

    @classmethod
    def create_client(cls, level: Level, endpoint: str) -> Self:
        """
        Creates a client instance with the specified level and endpoint.
        Args:
            level (str): The level of the client.
            endpoint (str): The endpoint for the client.
        Returns:
            Tuple[str, Self]: A tuple containing the level and the created client instance.
        """

        return cls(endpoint, level)

    def filter_content(self, content: str):
        """
        Filters the given content based on predefined categories and severity levels.
        Args:
            content (str): The text content to be analyzed and filtered.
        Returns:
            tuple: A tuple containing a boolean and a string. The boolean indicates whether the content
               meets the filtering criteria (True if it does, False otherwise). The string represents
               the category of the content if it meets the criteria.
        Raises:
            HttpResponseError: If there is an error during the text analysis process.
        """

        options = AnalyzeTextOptions(language="por", text_content=content)
        try:
            response = self.client.analyze_text(options)
        except HttpResponseError as e:
            if e.error:
                logger.error("Error code: %s", e.error.code)
                logger.error("Error message: %s", e.error.message)
                raise
            logger.error("Analyze text failed.")
            raise

        for item in response.categories_analysis:
            if (item.severity or 0) >= self.level.value:
                return (True, item.category)
        return (False, None)


class ContentFilteringApp:

    def __init__(self, blocklist: str):
        """
        Initializes the content filter with a blocklist and sets up the main and secondary filters.
        Args:
            blocklist (str): The blocklist to be used for filtering content.
        """

        self.main_filter = ContentFilterFactory.create_client(
            Level.MEDIUM, os.getenv("AZURE_CONTENTSAFETY_ENDPOINT", "")
        )
        self.secondary_filter = ContentFilterFactory.create_client(
            Level.LOW, os.getenv("AZURE_CONTENTSAFETY_ENDPOINT", "")
        )
        self.blocklist = blocklist

    def evaluate_content(self, content: str):
        """
        Evaluates the given content using primary and secondary filters, and a model evaluation.
        The method first applies the primary filter to the content. If the primary filter
        returns a positive result, it then applies the secondary filter. If the secondary
        filter also returns a positive result, it further evaluates the content using a 
        model evaluation. If the model evaluation is positive, the content is added to 
        the blocklist with the associated category and the method returns None. Otherwise, 
        it returns the original content.
        Args:
            content (str): The content to be evaluated.
        Returns:
            str or None: The original content if it passes the filters and model evaluation,
                         otherwise None if the content is added to the blocklist.
        """
        
        primary_result, category = self.main_filter.filter_content(content)
        if primary_result:
            secondary_result, category = self.secondary_filter.filter_content(content)
            if secondary_result:
                if self.model_evaluation(content):
                    self.add_to_blocklist(content, category)
                    return None
        return content

    def model_evaluation(self, content: str):
        """
            Evaluates the given content for harmfulness using an external API.
            This method sends the content to a chat completion client, which evaluates
            whether the content is harmful or not. The client is configured with an
            endpoint and credentials. The response from the client is checked to see
            if it indicates that the content is harmful.
            Args:
                content (str): The content to be evaluated.
            Returns:
                bool: Returns False if the content is deemed harmful, otherwise True.
            Raises:
                requests.exceptions.RequestException: If there is an error during the API request.
        """

        client = ChatCompletionsClient(
            endpoint=PHI_KEY or "",
            credential=DefaultAzureCredential()
        )
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": """
                        You are a evaluation assistant.\n
                        Check the content below and provide feedback if it is harmfull or not.\n
                        **Answer only 'Harmfull' or 'Not Harmfull'**.
                    """
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            "max_tokens": 15,
            "temperature": 0.1,
            "presence_penalty": 0,
            "frequency_penalty": 0
            }
        try:
            response = client.complete(payload)
            if response.choices[0].message.content == "Harmfull":
                return False
        except requests.exceptions.RequestException as e:
            logger.error("Error during PHI API request: %s", e)
            raise
        return True

    def add_to_blocklist(self, text: str, category: str | None):
        """
        Adds a text item to the blocklist with an optional category description.
        Args:
            text (str): The text to be added to the blocklist.
            category (str | None): An optional description or category for the blocklist item.
        Returns:
            None
        """
        
        blocklist_name = self.blocklist
        blocklist_item = TextBlocklistItem(description=category, text=text)
        options = AddOrUpdateTextBlocklistItemsOptions(blocklist_items=[blocklist_item])
        self.main_filter.blocklist.add_or_update_blocklist_items(blocklist_name, options)



def client_code(blocklist, content):
    """
    The client code works with an instance of a concrete creator, albeit through its base interface.
    """

    app = ContentFilteringApp(blocklist)
    return app.evaluate_content(content)
