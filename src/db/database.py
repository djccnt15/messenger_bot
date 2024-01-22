from contextlib import contextmanager

from sqlalchemy.engine import URL, create_engine
from sqlalchemy.orm import sessionmaker

from src.config import configs

db_config = configs.config.db

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername=db_config.drivername,
    username=db_config.username if db_config.username else None,
    password=db_config.password if db_config.password else None,
    host=db_config.host if db_config.host else None,
    port=int(db_config.port) if db_config.port else None,
    database=db_config.database,
)

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=db_config.echo,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
