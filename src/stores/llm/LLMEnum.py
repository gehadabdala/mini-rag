from enum import Enum


class LLMEnum(Enum):
    """
    Enum for LLM types.
    """

    OPENAI = "openai"
    COHERE = "cohere"
