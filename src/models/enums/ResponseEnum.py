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
