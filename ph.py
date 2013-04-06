#! /usr/bin/env python

import os
import sys
import json

import irc.client

class Grouphugs():

    def __init__(self, server, channel):

        print("WELCOME TO GH.")

        try:
            config_file = 'config.json'
            with open(config_file) as f:
                self.options = json.loads(f.read())
        except OSError:
            print("Couldn't find the configuration file, tried: %s" % os.path.abspath(config_file))
            raise SystemExit(1)

        client = irc.client.IRC()
        try:
            connection = client.server().connect(self.options['server'], self.options['port'], self.options['nickname'])
        except irc.client.ServerConnectionError:
            print(sys.exc_info()[1])
            raise SystemExit(1)

        connection.add_global_handler("welcome", self.on_connect)
        connection.add_global_handler("disconnect", self.on_disconnect)

        client.process_forever()

    def on_connect(self, connection, event):
        connection.join(self.options['channel'])

    def on_disconnect(self, connection, event):
        raise SystemExit()

if __name__ == '__main__':
    ph = Grouphugs('localhost', '#test')
