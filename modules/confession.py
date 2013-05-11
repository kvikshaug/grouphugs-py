from bs4 import BeautifulSoup
import requests
import re

class Module():
    """The original confession module (kind of)"""

    ROOT_URL = "http://www.roofessions.com"

    def __init__(self, gh):
        self.gh = gh
        self.gh.add_trigger("ph", self.confession)

    def confession(self, sender, channel, message, spam):
        # Get random confession list
        r = requests.get("%s/random.html" % self.ROOT_URL)
        doc = BeautifulSoup(r.text)
        confession = doc.find(lambda e: e.name == 'div' and e.has_key('class') and e['class'] == ['cnfContent'])
        url = confession.h3.a['href']

        # Get the specific confession
        r = requests.get("%s%s" % (self.ROOT_URL, url))
        doc = BeautifulSoup(r.text)
        confession = doc.find(lambda e: e.name == 'div' and e.has_key('class') and e['class'] == ['cnfContent'])
        confession_text = '\n'.join([c.text for c in confession.children if c.name == 'p'])
        confession_text = re.sub(r"<[^>]*>", "", confession_text)
        self.gh.privmsg(channel, confession_text, spam)
