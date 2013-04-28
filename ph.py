#! /usr/bin/env python

# stdlib
import os
import json
import signal

# 3rd party libs
import lurklib
from events import Events

# local code
from logger import logger

class Grouphugs(lurklib.Client):
    def __init__(self, options, *args, **kwargs):
        super(Grouphugs, self).__init__(*args, **kwargs)
        self.options = options
        self.events = Events()

        def shutdown_handler(signum, frame):
            logger.info("Caught shutdown signal, shutting down.")
            self.quit("Caught shutdown signal, shutting down.")

        # Attach management signals
        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)

    # Abstractions for lurklibs silly ways to do some things

    def is_op(self, nick, channel):
        return nick in self.channels[channel]['USERS'] and '@' in self.channels[channel]['USERS'][nick][2]

    # lurklibs event methods
    # We're not overriding all of them - for an exhaustive list, see lurklib/__init__.py

    def on_connect(self):
        for channel in self.options['channels']:
            self.join_(channel)

    def on_join(self, sender, channel):
        self.events.on_join(sender, channel)

    def on_part(self, sender, channel, reason):
        self.events.on_part(sender, channel, reason)

    def on_chanmsg(self, sender, channel, message):
        self.events.on_chanmsg(sender, channel, message)

    def on_privmsg(self, sender, message):
        self.events.on_privmsg(sender, message)

    def on_kick(self, sender, channel, who, reason):
        self.events.on_kick(sender, channel, who, reason)

    def on_nick(self, sender, new_nick):
        self.events.on_nick(sender, new_nick)

    def on_quit(self, sender, reason):
        self.events.on_quit(sender, reason)

if __name__ == '__main__':
    try:
        config_file = 'config.json'
        with open(config_file) as f:
            options = json.loads(f.read())
    except OSError:
        logger.error("Couldn't find the configuration file, tried: %s" % os.path.abspath(config_file))
        raise SystemExit(1)

    ph = Grouphugs(
        options,
        server=options['server'],
        port=options['port'],
        nick=tuple(options['nicks']),
        tls=False)

    # Instantiate defined modules
    for name, options in ph.options['modules'].items():
        module = __import__('modules.%s' % name, fromlist=[''])
        module.Module(ph)

    ph.mainloop()
