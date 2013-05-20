from datetime import datetime

class Module():
    """You know what the seen module does, fool"""

    def __init__(self, gh):
        self.gh = gh
        self.gh.add_trigger("seen", self.seen)
        self.gh.events.on_join += self.on_join
        self.gh.events.on_part += self.on_part
        self.gh.events.on_chanmsg += self.on_chanmsg
        self.gh.events.on_kick += self.on_kick
        self.gh.events.on_nick += self.on_nick
        self.gh.events.on_quit += self.on_quit
        self.history = {}

    def seen(self, sender, channel, message, spam):
        for nick in message.split():
            if not channel in self.history or not nick in self.history[channel]:
                self.gh.privmsg(channel, "I haven't seen %s do anything here." % nick)
                return

            self.gh.privmsg(channel, "%s %s at %s" % (
                nick,
                self.history[channel][nick]['action'],
                self.history[channel][nick]['dt'].strftime('%H:%M %d.%m.%Y')
            ))

    def on_join(self, sender, channel):
        if not channel in self.history:
            self.history[channel] = {}
        self.history[channel][sender[0]] = {
            'action': 'joined the channel',
            'dt': datetime.now()
        }

    def on_part(self, sender, channel, reason):
        if not channel in self.history:
            self.history[channel] = {}
        self.history[channel][sender[0]] = {
            'action': 'left the channel, saying "%s"' % reason,
            'dt': datetime.now()
        }

    def on_chanmsg(self, sender, channel, message):
        if not channel in self.history:
            self.history[channel] = {}
        self.history[channel][sender[0]] = {
            'action': 'said "%s"' % message,
            'dt': datetime.now()
        }

    def on_kick(self, sender, channel, who, reason):
        if not channel in self.history:
            self.history[channel] = {}
        self.history[channel][sender[0]] = {
            'action': 'got kicked by %s for "%s"' (who, reason),
            'dt': datetime.now()
        }

    def on_nick(self, sender, new_nick):
        # Record the event only in the channels we currently see them in
        for channel, contents in self.gh.channels.items():
            if new_nick in contents['USERS']:
                self.history[channel][sender[0]] = {
                    'action': 'changed nick to %s' % new_nick,
                    'dt': datetime.now()
                }
                self.history[channel][new_nick] = {
                    'action': 'changed nick from %s' % sender[0],
                    'dt': datetime.now()
                }

    def on_quit(self, sender, reason):
        # We get the event after they quit, so we don't know which of our channels we actually have this user in.
        # For now, record it in the channels we've already recorded events for the same user.
        # So if someone joins and parts a channel, while staying in another channel we're in, and then quits, calling
        # !seen in the first channel will 'leak' the quit information.
        for channel, users in self.history.items():
            if sender[0] in users:
                self.history[channel][sender[0]] = {
                    'action': 'disconnected, saying "%s"' % reason,
                    'dt': datetime.now()
                }
