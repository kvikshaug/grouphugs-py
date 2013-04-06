#! /usr/bin/env python

# stdlib
import os
import json
import signal

# 3rd party libs
import irc.client

# local ocde
from logger import logger

class Grouphugs():
    def __init__(self):
        try:
            config_file = 'config.json'
            with open(config_file) as f:
                self.options = json.loads(f.read())
        except OSError:
            logger.error("Couldn't find the configuration file, tried: %s" % os.path.abspath(config_file))
            raise SystemExit(1)

        client = irc.client.IRC()
        try:
            self.connection = client.server().connect(self.options['server'], self.options['port'], self.options['nickname'])
        except irc.client.ServerConnectionError as e:
            logger.error(e)
            raise SystemExit(1)

        # Attach management signals
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)

        self.connection.add_global_handler("welcome", self.on_connect)
        client.process_forever()

    def on_connect(self, connection, event):
        self.connection.join(self.options['channel'])

    def shutdown_handler(self, signum, frame):
        logger.info("Caught shutdown signal, shutting down.")
        if self.connection.is_connected():
            self.connection.quit("Caught shutdown signal, laters.")

if __name__ == '__main__':
    ph = Grouphugs()
