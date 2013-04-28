Modules
=======

Let's add an example module, ``echo``, which will echo what anyone says in any channel.

1. Create the file ``modules/echo.py``.

::

    class Module():
        """Example module that echos all input"""

        def __init__(self, gh):
            self.gh = gh

Note:

* A modules class name must always be ``Module``. The module name is defined in its *python module* (the file name).
* The ``__init__`` method takes one argument (``gh``) which is the bot instance.

2. To load the module, add an entry for it in ``config.json``:

::

    {
        ...

        "modules": {
            ...

            "echo": {}
        }
    }

Note that the key name **must** match the file name.

Events
------

``gh`` uses `Events`_. It defines some of `lurklibs events`_, like ``on_chanmsg``, and modules can listen for any of those.

.. _Events: https://pypi.python.org/pypi/Events/0.1.0
.. _lurklibs events: https://github.com/LK-/lurklib/blob/a861f35d880140422103dd78ec3239814e85fd7e/lurklib/__init__.py#L99

3. Let's extend our ``echo`` module to listen for channel messages.

.. code-block:: python

    class Module():
        """Example module that echos all input"""

        def __init__(self, gh):
            self.gh = gh
            self.gh.events.on_chanmsg += self.on_chanmsg

        def on_chanmsg(self, sender, channel, message):
            self.gh.privmsg(channel, message))

We defined the new ``on_chanmsg`` function, and added it to gh's ``on_chanmsg`` event (the ``events`` field). Note that we had to copy the ``on_chanmsg`` method signature from ``gh.py``.

We then call ``privmsg`` on the bot (that's a ``lurklib`` method) with the same channel and message.

Module configuration
--------------------

The module entry in ``config.json`` can store module configurations. Let's add a ``prefix`` options which will prefix all echoed messages with some string.

In ``config.json``:

::

    {
        ...

        "modules": {
            ...

            "echo": {
                "prefix": "foo "
            }
        }
    }

Then we update ``on_chanmsg`` in ``echo`` to get the config through ``gh``s ``option`` field:

::

    def on_chanmsg(self, sender, channel, message):
        self.gh.privmsg(channel, "%s%s" % (self.gh.options['modules']['echo']['prefix'], message))

Triggers
--------

So far, so simple. However, many modules want to listen for some trigger keyword instead of every message. Let's rewrite our module to only echo when someone triggers it with the keyword **echo**.

::

    class Module():
        """Example module that echos all input"""

        def __init__(self, gh):
            self.gh = gh
            self.gh.add_trigger("echo", self.on_echo)

        def on_echo(self, sender, channel, message):
            self.gh.privmsg(channel, "%s: %s" % (sender[0], message))

* This will now call the ``on_echo`` method when a users triggers it (by saying "!echo ")
* The method signature is equal to ``on_chanmsg``
* The "!echo " part is stripped from the ``message`` argument
* Note that the ``sender`` argument isn't just the nick, but rather a tuple of (nick, ident, host)
