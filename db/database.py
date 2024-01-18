from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQL_ALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_ID}:{DB_PW}@"
    f"{DB_HOST}:{DB_PORT}/{DB}"
)

engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,
    encodings="utf-8"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
