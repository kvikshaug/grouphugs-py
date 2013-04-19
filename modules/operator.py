class Operator():
    """Automatically give op to configured nicks"""

    def __init__(self, ph):
        self.ph = ph
        self.ph.events.on_join += self.on_join
        self.ph.events.on_chanmsg += self.on_chanmsg
        self.ph.events.on_nick += self.on_nick

    def on_join(self, sender, channel):
        self.give_op(sender[0], [channel])

    def on_chanmsg(self, sender, channel, message):
        self.give_op(sender[0], [channel])

    def on_nick(self, sender, new_nick):
        self.give_op(new_nick, self.ph.options['channels'])

    def give_op(self, nick, channels):
        if nick in self.ph.options['modules']['operator']['operators']:
            # Don't bother checking if the bot is actually op
            for channel in channels:
                self.ph.cmode(channel, "+o %s" % nick)
