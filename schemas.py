from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any
from enum import Enum

class QAItem(BaseModel):
    id: int
    question: str
    answer: str
    difficulty: Literal["basic", "intermediate", "advanced"]
    type: Literal["theoretical", "practical", "code", "application"]

class QAList(BaseModel):
    items:List[QAItem]

class FieldType(str, Enum):
    string = "string"
    number = "number"
    array = "array"
    # object = "object"
    boolean = "boolean"
    # date = "date"

class SchemaField(BaseModel):
    key: str = Field(..., description="The unique identifier for the field")
    type: FieldType = Field(..., description="The data type of the field")
    description: str = Field(..., description="Some descriptive information for the field")

class DatasetSchema(BaseModel):
    generated_schema: list[SchemaField]

class DatasetRecords(BaseModel):
    dataset:List[Dict[str, Any]]