Lurklib patches
===============

``gh`` uses the `lurklib`_ IRC lib. It seems to be one of the most mature py3 irc libs out there at the time of this writing, however `the project went inactive`_ 11 months ago and some bugs have been found.

.. _the project went inactive: https://github.com/LK-/lurklib
.. _lurklib: https://pypi.python.org/pypi/lurklib/1.0.1

Check mode characters, not symbols
----------------------------------
When lurklib receives a channel mode change, it parses the mode string and updates its internal state. However, in `the parsing logic`_, it checks that the `new mode`_ is one of the available `priv_types`_. That seems to be a bug; e.g. for setting an operator, the mode is ``o`` while the priv_type is ``@``.

This patch adds a ``priv_type_modes`` field with the matching modes ``('q', 'a', 'o', 'h', 'v')``, and checks for that instead in ``parse_cmode_string``.

:download:`Download the patch here <lurklib_patches/0001-Check-mode-characters-not-symbols.patch>`.

.. _the parsing logic: https://github.com/LK-/lurklib/blob/a861f35d880140422103dd78ec3239814e85fd7e/lurklib/channel.py#L405
.. _new mode: https://github.com/LK-/lurklib/blob/a861f35d880140422103dd78ec3239814e85fd7e/lurklib/channel.py#L422
.. _priv_types: https://github.com/LK-/lurklib/blob/a861f35d880140422103dd78ec3239814e85fd7e/lurklib/variables.py#L43
