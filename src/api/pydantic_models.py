from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class ModelName(str, Enum):
    GPT4_O = "gpt-4o"
    GPT4_O_MINI = "gpt-4o-mini"
    LLAMA_3_2_7B = "llama3.2:latest"
    LLAMA_3_2_1B = "llama3.2:1b"
    MISTRAL_7B_INS = "mistral:7b-instruct"

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT4_O_MINI)

class QueryResponse(BaseModel):
    answer: dict
    session_id: str
    model: ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int