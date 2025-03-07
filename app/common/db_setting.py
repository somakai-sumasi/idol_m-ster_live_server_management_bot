from config.db import DB_NAME
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import json

DATABASE = "sqlite:///" + DB_NAME

ENGINE = create_engine(
    DATABASE,
    echo=False,
    _json_serializer=lambda x: json.dumps(x, ensure_ascii=False),
)
Base = declarative_base()

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))
