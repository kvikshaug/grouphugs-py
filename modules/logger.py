import logging
import logging.config

from modules.database import Database


class Module(Database):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.bot.events.on_chanmsg += self.on_chanmsg
        self.log = logging.getLogger(__name__)
        self.table = self.hstore_table_for('logs')

    def on_chanmsg(self, sender, channel, message):
        msg = {'sender': '{0}!{1}@{2}'.format(*sender), 'channel': channel, 'message': message}
        self.log.debug('inserting %s', msg)
        with self.engine.connect() as c:
            c.execute(self.table.insert(), data=msg)
