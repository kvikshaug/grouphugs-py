import unittest
from gh import Grouphugs


class GrouphugsTest(unittest.TestCase):
    def setUp(self):
        self.gh = Grouphugs()

    def test_wrap_sender_should_return_namedtuple(self):
        sender = ('foo', 'bar', 'baz')
        wrapped = self.gh.wrap_sender(sender)

        self.assertEqual(wrapped.nick, sender[0])
        self.assertEqual(wrapped.ident, sender[1])
        self.assertEqual(wrapped.host, sender[2])
