Development
============

These steps assume that you're using virtualenv.

1. Clone the repository::

    $ git clone https://github.com/SketchingDev/Doodle-Dashboard.git
    $ cd doodle-dashboard

2. Prepare project dependencies::

    $ make dev
    $ export PYTHONPATH=`pwd`

3. See usage help::

    $ python doodledashboard/cli.py


ImportError: No module named
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you keep getting the ImportError when building the project check that you
haven't already installed the application via pip, otherwise you might be pulling
in the doodle dashboard classes from your local pip packages.

Remove the library with::

    $ sudo rm -rf /Library/Python/3.6/site-packages/doodledashboard/