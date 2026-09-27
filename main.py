
from fastapi import FastAPI

from app.database import Base, engine
from app.models.user_model import User

from app.routes.rag_routes import router as rag_router
from app.routes.document_routes import router as document_router

Base.metadata.create_all(
    bind=engine
)



app = FastAPI()



app.include_router(rag_router)
app.include_router(document_router)
print("FastAPI app initialized")