Getting started
===============

You'll need `git`_, `virtualenv`_, `pip`_ and `python 3`_:

.. _git: http://git-scm.com/
.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _pip: http://www.pip-installer.org/en/latest/
.. _python 3: http://www.python.org/download/releases/3.3.1/

::

    git clone git://github.com/kvikshaug/grouphugs-py.git
    cd grouphugs-py/
    virtualenv env
    . env/bin/activate # or whatever your shell needs
    pip install -r requirements.txt
    vim config.json
    # Apply lurklib patches here
    python gh.py

Applying :doc:`patches </lurklib_patches>`
------------------------------------------

::

    cd env/lib/python3.3/site-packages/
    wget ... # Download the patches
    patch -p1 < 0001-Check-mode-characters-not-symbols.patch
    rm -i *.patch
