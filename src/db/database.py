from contextlib import contextmanager

from sqlalchemy.engine import URL, create_engine
from sqlalchemy.orm import sessionmaker

from src.config import config

db_info = config.parser["DB"]

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername=db_info["drivername"],
    username=db_info["username"] if db_info["username"] else None,
    password=db_info["password"] if db_info["password"] else None,
    host=db_info["host"] if db_info["host"] else None,
    port=int(db_info["port"]) if db_info["port"] else None,
    database=db_info["database"],
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
