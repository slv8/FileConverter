from enum import StrEnum


class ConversionStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


UnfinishedConversionStatuses = {ConversionStatus.PENDING, ConversionStatus.IN_PROGRESS}


class FileOutputExtension(StrEnum):
    PDFX = "pdfx"
    JSONL = "jsonl"
    BINX = "binx"


class FileInputExtension(StrEnum):
    MFILE = "mfile"


class UploadStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
