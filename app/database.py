from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread":False
    }
 )

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# it gives each request a database session and closes it afterward
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()