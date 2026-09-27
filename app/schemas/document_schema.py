from pydantic import BaseModel
class DocumentResponse(BaseModel):
    id:str
    filename:str
    path:str
    chunks:int

class DocumentUploadResponse(BaseModel):
    message:str
    document:DocumentResponse

class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]