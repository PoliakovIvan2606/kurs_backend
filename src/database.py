from typing import Annotated

from sqlalchemy import create_engine, String, Integer
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
# from config import settings


sync_engine = create_engine(
    # url=settings.DATABASE_URL_psycopg,
    url="sqlite:///data.db",
    echo=True,
)

session_factory = sessionmaker(sync_engine)
















str_10 = Annotated[str, 10]
str_17 = Annotated[str, 17]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_10: String(10),
        str_17: String(17),
    }

# Base.metadata.create_all(sync_engine)
