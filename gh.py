#! /usr/bin/env python

# stdlib
import signal
import re
import logging
import logging.config
from collections import namedtuple

# 3rd party libs
from events import Events
from irc import Irc

# local code
import config

Sender = namedtuple('Sender', ['nick', 'ident', 'host'])

class Grouphugs(object):
    def __init__(self):
        self.run_forever = True
        self.events = Events()
        self.triggers = []
        self.max_spam_lines = 5
        self.logger = logging.getLogger(__name__)
        self.irc = Irc(config.SERVER, config.PORT, config.NICKS)

        def shutdown_handler(signum, frame):
            self.run_forever = False
            self.logger.info("Caught shutdown signal, shutting down.")
            self.quit("Caught shutdown signal, shutting down.")

        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)

    def connect_and_loop(self):
        try:
            self.irc.connect()
        except Exception as e:
            logger.exception('Exception from asyncore loop', e)

    def is_op(self, nick, channel):
        return nick in self.channels[channel]['USERS'] and '@' in self.channels[channel]['USERS'][nick][2]

    def privmsg(self, channel, message, spam=False):
        message = re.sub(r'\t', '    ', message) # Replace tabs with spaces

        if not spam and len(message) > 510 * self.max_spam_lines:
            self.irc.privmsg(channel, "This would spam the channel with {} lines, replace ! with @ if you really want that.".format(len(message) / 510))
            return

        self.irc.privmsg(channel, message)

    def add_trigger(self, trigger, func):
        self.triggers.append({'trigger': trigger, 'func': func})

    def on_connect(self):
        for channel in config.CHANNELS:
            self.irc.write('JOIN {}'.format(channel))

    def on_join(self, sender, channel):
        self.events.on_join(self.wrap_sender(sender), channel)

    def on_part(self, sender, channel, reason):
        self.events.on_part(self.wrap_sender(sender), channel, reason)

    def on_chanmsg(self, sender, channel, message):
        self.events.on_chanmsg(self.wrap_sender(sender), channel, message)
        for trigger in self.triggers:
            if message.startswith("!%s" % trigger['trigger']):
                trigger['func'](self.wrap_sender(sender), channel, message[len(trigger['trigger']) + 1:].strip(), spam=False)
            elif message.startswith("@%s" % trigger['trigger']):
                trigger['func'](self.wrap_sender(sender), channel, message[len(trigger['trigger']) + 1:].strip(), spam=True)

    def on_privmsg(self, sender, message):
        self.events.on_privmsg(self.wrap_sender(sender), message)

    def on_kick(self, sender, channel, who, reason):
        self.events.on_kick(self.wrap_sender(sender), channel, who, reason)

    def on_nick(self, sender, new_nick):
        self.events.on_nick(self.wrap_sender(sender), new_nick)

    def on_quit(self, sender, reason):
        self.events.on_quit(self.wrap_sender(sender), reason)

if __name__ == '__main__':
    logging.config.dictConfig(config.LOGGING)
    logger = logging.getLogger(__name__)

    gh = Grouphugs()

    # Instantiate defined modules
    for name, options in config.MODULES.items():
        module = __import__('modules.%s' % name, fromlist=[''])
        module.Module(gh)

    gh.connect_and_loop()
