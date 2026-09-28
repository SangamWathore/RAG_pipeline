
from fastapi import FastAPI

from app.database import Base, engine
from app.routes.rag_routes import router as rag_router
from app.routes.document_routes import router as document_router
from app.routes.auth_routes import router as auth_router

Base.metadata.create_all(
    bind=engine
)



app = FastAPI()



app.include_router(rag_router)
app.include_router(document_router)
app.include_router(auth_router)