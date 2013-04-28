class Module():
    """Example module that echos all input"""

    def __init__(self, ph):
        self.ph = ph
        self.ph.events.on_chanmsg += self.on_chanmsg
        self.ph.add_trigger("hello", self.on_hello)

    def on_chanmsg(self, sender, channel, message):
        self.ph.privmsg(channel, "%s%s" % (self.ph.options['modules']['echo']['prefix'], message))

    def on_hello(self, sender, channel, message):
        self.ph.privmsg(channel, "Hello %s, %s to you too." % (sender[0], message))
