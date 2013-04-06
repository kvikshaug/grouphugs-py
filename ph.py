#! /usr/bin/env python

# stdlib
import os
import json

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
            connection = client.server().connect(self.options['server'], self.options['port'], self.options['nickname'])
        except irc.client.ServerConnectionError as e:
            logger.error(e)
            raise SystemExit(1)

        connection.add_global_handler("welcome", self.on_connect)
        client.process_forever()

    def on_connect(self, connection, event):
        connection.join(self.options['channel'])

if __name__ == '__main__':
    ph = Grouphugs()
