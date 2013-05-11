Getting started
===============

You'll need `git`_, `virtualenv`_, `pip`_ and `python 3`_.

.. _git: http://git-scm.com/
.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _pip: http://www.pip-installer.org/en/latest/
.. _python 3: http://www.python.org/download/releases/3.3.1/

Download::

    git clone git://github.com/kvikshaug/grouphugs-py.git
    cd grouphugs-py/

Set up the environment::

    virtualenv env
    . env/bin/activate # or whatever your shell needs

Install the requirements. **Note that lurklib will fail because our fork isn't in pypi.**
::

    pip install -r requirements.txt

Install our lurklib fork::

    git clone git://github.com/kvikshaug/lurklib.git
    pushd lurklib/
    python setup.py install
    popd
    rm -r lurklib/

Edit the config to your likings::

    vim config.json

Fire up the bot::

    python gh.py
