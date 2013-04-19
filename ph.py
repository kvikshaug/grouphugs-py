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
import modules

class Grouphugs(lurklib.Client):
    def __init__(self, options, *args, **kwargs):
        super(Grouphugs, self).__init__(*args, **kwargs)
        self.options = options
        self.events = Events()

        def shutdown_handler(signum, frame):
            logger.info("Caught shutdown signal, shutting down.")
            self.quit("Caught shutdown signal, laters.")

        # Attach management signals
        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)

    def on_connect(self):
        self.join_(self.options['channel'])

    def on_chanmsg(self, sender, channel, message):
        self.events.on_chanmsg(sender, channel, message)

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
    modules.init(ph)
    ph.mainloop()
