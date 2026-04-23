from .BaseController import BaseController

# from models.db_schemas import Project, DataChunk
from models.db_schemes import project, datachunk
from typing import List
from stores.llm.LLMEnums import DocumentTypeEnum
import json


class NLPController(BaseController):

    def __init__(
        self, vectordb_client, generation_client, embedding_client, template_parser
    ):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()

    def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.embedding_client.get_collection_info(
            collection_name=collection_name
        )

        return json.loads(  # convert into dict
            json.dumps(
                collection_info, default=lambda x: x.__dict__
            )  # convert into string
        )
        # Convert to JSON-serializable format

    def index_into_vector_db(
        self, project: Project, chunks: List[DataChunk], do_reset: bool = False
    ):

        # step 1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step 2: manage items
        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]
        # التعديل هنا: اتأكدي إنك بتاخدي الـ embeddings صح
        response = self.embedding_client.embed_text(
            text=texts, document_type=DocumentTypeEnum.DOCUMENT.value
        )

        vectors = response.embeddings if hasattr(response, "embeddings") else response

        # step 3: create collection if not exist
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )

        # step 4: insert into vector db
        _ = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
        )

        return True

    def search_vector_db(self, project: Project, text: str, limit: int = 10):
        collection_name = self.create_collection_name(project_id=project.project_id)

        vector = self.embedding_client.embed_text(
            text=text, document_type=DocumentTypeEnum.QUERY.value
        )

        if not vector or len(vector) == 0:
            return False

        search_results = self.vectordb_client.search_by_vector(
            collection_name=collection_name, vector=vector, limit=limit
        )
        if not search_results:
            return False

        return search_results

    def answer_rag_question(self, project: Project, query: str, limit: int = 10):
        answer, full_prompt, chat_history = None, None, None
        # step 1: retrieve related documents
        retrieved_documents = self.search_vector_db(
            project=project, text=query, limit=limit
        )

        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history

        # step 2: construct LLM prompt
        system_prompt = self.template_parser.get("rag", "system_prompt")

        # document_prompts =[]
        # for idx, doc in enumerate(retrieved_documents):
        #     document_prompts.append(
        #         self.template_parser.get("rag","document_prompts",{
        #             "doc_num": idx +1,
        #             "chunk_text": doc.text,
        #         })
        #     )

        document_prompt = "\n".join(
            [
                self.template_parser.get(
                    "rag",
                    "document_prompt",
                    {
                        "doc_num": idx + 1,
                        "chunk_text": doc.text,
                    },
                )
                for idx, doc in enumerate(retrieved_documents)
            ]
        )

        footer_prompt = self.template_parser.get("rag", "footer_prompt")

        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

        full_prompt = "\n\n".join([document_prompt, footer_prompt])

        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history,
        )

        return answer, full_prompt, chat_history
