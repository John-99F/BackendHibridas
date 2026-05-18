from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USER = "johnu1604_roottest16"
PASSWORD = "Root0234"
HOST = "mysql-johnu1604.alwaysdata.net"
PORT = "3306"
DB = "johnu1604_hibridas"

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"charset": "utf8mb4"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()