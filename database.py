from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USER = "root"
PASSWORD = ""
HOST = "localhost"
PORT = "3306"
DB = "socialred"

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"charset": "utf8mb4"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()