from db_model import *
import config

#----------------------------
# Turn Foreign Key Constraints ON for
# each connection.
#----------------------------

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

#----------------------------
# Create the engine
#----------------------------
from sqlalchemy import create_engine
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)

#----------------------------
# Create the Schema
#----------------------------

Base.metadata.create_all(engine)