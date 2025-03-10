import enum
from typing import TypeVar

from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class FileType(enum.Enum):
    CSV = "csv"
    XLSX = "xlsx"
    XLS = "xls"
    JSON = "json"
    DOC = "doc"
    DOCX = "docx"
    PDF = "pdf"
    PPT = "ppt"
    PPTX = "pptx"
