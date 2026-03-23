from abc import ABC, abstractmethod


class LLMInterface(ABC):

    @abstractmethod
    def set_generate_model(
        self, model_id: str
    ):  # اي حد بعدي مجبر يكون عنده نفس الداله دي
        pass

    @abstractmethod
    def set_embedding_model(
        self, model_id: str
    ):  # اي حد بعدي مجبر يكون عنده نفس الداله دي
        pass

    @abstractmethod
    def generate_text(
        self, prompt: str, max_tokens: int = 100, temperature: float = None
    ):  # temperature  0:1
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: str):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass
