from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./todo.db"

''' 
Desabilitar o uso de threads para SQLite, pois o Flask pode usar multiplas threads e
causar erros de conexao.
'''
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Criar uma sessão local para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base é a classe base para os modelos do SQLAlchemy
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from src.models.task import Task  # noqa: F401 — ensures table is registered
    Base.metadata.create_all(bind=engine)
