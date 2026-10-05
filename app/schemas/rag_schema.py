from pydantic import BaseModel, Field
from typing import Optional

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class Source(BaseModel):
    source: Optional[str] = None
    page: Optional[int] = None
    content: str

class AskResponse(BaseModel):
    question:str
    answer:str
    sources: list[Source] = Field(default_factory=list)
