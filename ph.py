#! /usr/bin/env python

# stdlib
import os
import json
import signal

# 3rd party libs
import lurklib

# local ocde
from logger import logger

class Grouphugs(lurklib.Client):
    def __init__(self, options, *args, **kwargs):
        super(Grouphugs, self).__init__(*args, **kwargs)
        self.options = options

        # Attach management signals
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)

    def on_connect(self):
        self.join_(self.options['channel'])

    def shutdown_handler(self, signum, frame):
        logger.info("Caught shutdown signal, shutting down.")
        self.quit("Caught shutdown signal, laters.")

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
    ph.mainloop()
