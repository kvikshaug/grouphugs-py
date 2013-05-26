import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.ext.mutable import MutableDict

import logging
import logging.config

from modules.base import Base

class Module():
    def __init__(self, bot):
        self.bot = bot
        self.bot.events.on_chanmsg += self.on_chanmsg
        self.log = logging.getLogger(__name__)
        self.table = sa.Table('logs', Base.metadata,
                              sa.Column('id', sa.Integer, primary_key=True),
                              sa.Column('data', MutableDict.as_mutable(pg.HSTORE)))
        self.engine = sa.create_engine(self.bot.options['database_uri'])

    def on_chanmsg(self, sender, channel, message):
        msg = {'sender': '{0}!{1}@{2}'.format(*sender), 'channel': channel, 'message': message}
        self.log.debug('inserting %s', msg)
        with self.engine.connect() as c:
            c.execute(self.table.insert(), data=msg)
