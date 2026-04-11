from enum import Enum


class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "file validated successfully"
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_SIZE_EXCEEDS = "file size exceeds the limit"
    FILE_UPLOAD_SUCCESS = "success"
    FILE_UPLOAD_FAILED = "file upload failed"
    PROCESSING_SUCCESS = "file processing success"
    PROCESSING_FAILED = "file processing failed"
    NO_FILES_ERROR = "no files error"
    FILE_ID_ERROR = "no file found with this id "
    PROJECT_NOT_FOUND_ERROR = "project not found"
    INSERT_INTO_VECTORDB_ERROR = "insert_into_vectordb_error"
    INSERT_INTO_VECTORDB_SUCCESS = "insert_into_vectordb_success"
    VECTORDB_COLLECTION_RETRIVED = "vectordb_collection_retrived_successfully"
    VECTORDB_SEARCH_ERROR = "search_results_not_found"
    VECTORDB_SEARCH_SUCCESS = "search_results_successfully"
    RAG_ANSWER_ERROR = "rag_answer_error"
    RAG_ANSWER_SUCCESS = "rag_answer_success"
