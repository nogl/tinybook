import sqlalchemy.orm

from app.base_config import BaseConfig

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base: sqlalchemy.orm.DeclarativeBase
Base.query = db_session.query_property()

metadata = Base.metadata

