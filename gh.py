#! /usr/bin/env python

# stdlib
import signal
import re
import logging
import logging.config
from collections import namedtuple

# 3rd party libs
import lurklib
from events import Events

# local code
import config

Sender = namedtuple('Sender', ['nick', 'ident', 'host'])

class Grouphugs(lurklib.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run_mainloop_forever = True
        self.events = Events()
        self.triggers = []
        self.max_line_chars = 440
        self.max_spam_lines = 5
        self.logger = logging.getLogger(__name__)

        def shutdown_handler(signum, frame):
            self.run_mainloop_forever = False
            self.logger.info("Caught shutdown signal, shutting down.")
            self.quit("Caught shutdown signal, shutting down.")

        # Attach management signals
        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)

    def wrap_sender(self, sender):
        return Sender(*sender)

    def mainloop(self):
        while self.run_mainloop_forever:
            try:
                super().mainloop()
            except Exception as e:
                self.on_exeption(e)

    # Abstractions for lurklibs silly ways to do some things

    def is_op(self, nick, channel):
        return nick in self.channels[channel]['USERS'] and '@' in self.channels[channel]['USERS'][nick][2]

    def privmsg(self, channel, message, spam=False):
        # Insert newlines for every 'max_line_chars' chars without any newlines
        message = re.sub(r'([^\n]{%s})' % self.max_line_chars, r'\1\n', message)

        message = re.sub(r'\r', '', message)     # Remove carriage returns
        message = re.sub(r'\n+', '\n', message)  # Remove consecutive newlines
        message = re.sub(r'^\n', '', message)    # Remove leading newline
        message = re.sub(r'\n$', '', message)    # Remove trailing newline
        message = re.sub(r'\t', '    ', message) # Replace tabs with spaces

        # Send each line separately
        messages = message.split('\n')

        if not spam and len(messages) > self.max_spam_lines:
            super().privmsg(channel, "This would spam the channel with %s lines, replace ! with @ if you really want that." % len(messages))
            return

        for message in messages:
            super().privmsg(channel, message)

    # Custom events

    def add_trigger(self, trigger, func):
        self.triggers.append({'trigger': trigger, 'func': func})

    # lurklibs event methods
    # We're not overriding all of them - for an exhaustive list, see lurklib/__init__.py

    def on_connect(self):
        for channel in config.CHANNELS:
            self.join_(channel)

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

    def on_exeption(self, exception):
        logger.exception(exception)

if __name__ == '__main__':
    logging.config.dictConfig(config.LOGGING)
    logger = logging.getLogger(__name__)

    gh = Grouphugs(server=config.SERVER,
                   port=config.PORT,
                   nick=tuple(config.NICKS),
                   tls=False)

    # Instantiate defined modules
    for name, options in config.MODULES.items():
        module = __import__('modules.%s' % name, fromlist=[''])
        module.Module(gh)

    gh.mainloop()
