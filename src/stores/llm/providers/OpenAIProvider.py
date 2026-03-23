from ..LLMInterface import LLMInterface
from openai import OpenAI

class OpenAIProvider(LLMInterface):
    def __init__(self, api_key: str, api_url: str = None,
                        default_input_max_characters: int = 1000, default_output_max_characters: int = 2048):
           