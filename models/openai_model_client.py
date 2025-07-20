from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constants import MODEL_OPENAI, OPENAI_API_KEY


class ModelClient:
    """
    Singleton-style access to a shared instance of OpenAIChatCompletionClient.
    Prevents redundant instantiation and ensures consistent configuration.
    """
    _instance: OpenAIChatCompletionClient | None = None

    def __init__(self):
        raise RuntimeError("Use ModelClient.get_client() instead of instantiating directly.")

    @classmethod
    def get_client(cls) -> OpenAIChatCompletionClient:
        """
        Returns a cached instance of OpenAIChatCompletionClient.
        Creates one if it doesn't already exist.
        """
        if cls._instance is None:
            cls._instance = OpenAIChatCompletionClient(
                model=MODEL_OPENAI,
                api_key=OPENAI_API_KEY
            )
        return cls._instance
