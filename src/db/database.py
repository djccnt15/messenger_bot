from contextlib import contextmanager

from sqlalchemy.engine import URL, create_engine
from sqlalchemy.orm import sessionmaker

from src.config import configs

db_config = configs.config.db

SQLALCHEMY_DATABASE_URL = URL.create(**db_config.url)

engine = create_engine(url=SQLALCHEMY_DATABASE_URL, **db_config.engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
