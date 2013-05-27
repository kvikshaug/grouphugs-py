import config


class Module():
    """Automatically give op to configured nicks"""

    def __init__(self, gh):
        self.gh = gh
        self.gh.events.on_join += self.on_join
        self.gh.events.on_chanmsg += self.on_chanmsg
        self.gh.events.on_nick += self.on_nick

    def on_join(self, sender, channel):
        self.give_op(sender[0], [channel])

    def on_chanmsg(self, sender, channel, message):
        self.give_op(sender[0], [channel])

    def on_nick(self, sender, new_nick):
        self.give_op(new_nick, config.CHANNELS)

    def give_op(self, nick, channels):
        if nick in config.MODULES['operator']['operators']:
            # Don't bother checking if the bot is actually op
            for channel in channels:
                if self.gh.is_op(nick, channel):
                    # User already has op
                    continue

                self.gh.cmode(channel, "+o %s" % nick)
