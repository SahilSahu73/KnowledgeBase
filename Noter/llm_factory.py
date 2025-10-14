from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatAnthropic
from logger_config import logger
try:
    from langchain_groq import ChatGroq
except ImportError:
    logger.error("Could not import ChatGroq.")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    logger.error("Could not import ChatGoogleGenerativeAI")
from typing import Dict, Any


class LLMFactory:
    """
    Factory class to create LLM instances from different providers.
    """
    @staticmethod
    def create_llm(provider: str, model: str, **kwargs) -> Any:
        """
        Create an LLM instance from the specified provider

        Args:
            provider: LLM provider (openai, anthropic, groq, google)
            model: Model name to use
            **kwargs: Additional arguments to pass to the LLM constructor

        Returns:
            An initialized LLM instance

        Raises:
            ValueError: If provider is not supported
        """
        # set default parameters
        params = {
            "model": model,
            "max_tokens": kwargs.get("max_tokens", None),
            "temperature": kwargs.get("temperature", 0.1),
            "reasoning_format": kwargs.get("reasoning_format", "hidden")
        }

        # Add provider specific parameters
        if provider == "groq":
            if "ChatGroq" not in globals():
                raise ImportError("Groq package not installed. \
                                   Check if uv has added it properly or not.")

            return ChatGroq(**params)

        elif provider == "openai":
            return ChatOpenAI(**params)

        elif provider == "google":
            if "ChatGoogleGenerativeAI" not in globals():
                raise ImportError("Google GenAI package not installed. \
                                   Check if uv has added it properly or not.")

            return ChatGoogleGenerativeAI(**params)

        elif provider == "anthropic":
            return ChatAnthropic(**params)

        else:
            raise ValueError(f"Unsupported LLM provider: {provider}, \
            Supported providers are: openai, groq, google, anthropic.")

    @staticmethod
    def get_available_providers() -> Dict[str, list]:
        """
        Get available LLM providers and their supported models

        Returns: Dictionary of providers and their supported models
        """
        return {
            "openai": ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
            # The below models can be accessed through groq and I have selected only these because for this task we need to generate alot
            # of tokens within a minute. These models have a high Tokens Per Minute (TPM) rate through the API so it will be fast and free.
            "groq": ["llama-3.3-70b-versatile",
                     "mixtral-8x7b-32768",
                     "meta-llama/llama-4-scout-17b-16e-instruct",
                     "meta-llama/llama-prompt-guard-2-86m",
                     "moonshotai/kimi-k2-instruct",
                     "openai/gpt-oss-120b"
                     ],
            "google": ["gemini-2.5-flash", "gemini-pro-vision"]
        }
