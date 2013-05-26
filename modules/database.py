import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.declarative import declarative_base

import config

class Database():
    Base = declarative_base()

    def __init__(self):
        self.engine = sa.create_engine(config.DATABASE_URI)

    def hstore_table_for(self, name):
        return sa.Table(name, self.__class__.Base.metadata,
                        sa.Column('id', sa.Integer, primary_key=True),
                        sa.Column('data', MutableDict.as_mutable(pg.HSTORE)))
