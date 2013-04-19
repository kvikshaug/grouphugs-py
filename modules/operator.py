class Operator():
    """Automatically give op to configured nicks"""

    def __init__(self, ph):
        self.ph = ph
        self.ph.events.on_join += self.on_join
        self.ph.events.on_chanmsg += self.on_chanmsg
        self.ph.events.on_nick += self.on_nick

    def on_join(self, sender, channel):
        self.give_op(sender[0])

    def on_chanmsg(self, sender, channel, message):
        self.give_op(sender[0])

    def on_nick(self, sender, new_nick):
        self.give_op(new_nick)

    def give_op(self, nick):
        if nick in self.ph.options['modules']['operator']['operators']:
            # Don't bother checking if the bot is actually op
            self.ph.cmode(self.ph.options['channel'], "+o %s" % nick)
