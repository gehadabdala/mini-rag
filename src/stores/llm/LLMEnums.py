from enum import Enum


class LLMEnums(Enum):
    """
    Enum for LLM types.
    """

    OPENAI = "OPENAI"
    COHERE = "COHERE"


class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CoHereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"
    DoCUMENT = "search_document"
    QUERY = "search_query"


class DocumentTypeEnum(Enum):

    DOCUMENT = "document"
    QUERY = "query"
