from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URL = "sqlite:///./kavak.db"
        self.engine = create_engine(
            self.SQLALCHEMY_DATABASE_URL, 
            connect_args={"check_same_thread": False}
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )
        self.Base = declarative_base()

    def init_db(self):
        from src.core.entities import Car
        self.Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

db = Database()