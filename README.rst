Doodle-Dashboard: Simple dashboards for all!
============================================

.. image:: https://img.shields.io/pypi/v/doodle-dashboard.svg
    :target: https://pypi.org/project/doodle-dashboard/
    :alt: Latest version

.. image:: https://travis-ci.org/SketchingDev/Doodle-Dashboard.svg?branch=master
    :target: https://travis-ci.org/SketchingDev/Doodle-Dashboard
    :alt: Build status

.. image:: https://readthedocs.org/projects/doodle-dashboard/badge/?version=latest
    :target: https://doodle-dashboard.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

---------------

**Doodle-Dashboard** is used to create little dashboards that display useful information from multiple sources, like
Tweets from your favourite Twitterers, weather reports for your local area or breaking news.

.. image:: https://raw.githubusercontent.com/SketchingDev/Doodle-Dashboard/master/docs/_static/flow-diagram.png

Requirements
------------

  * `Python 3.5+ <https://www.python.org/downloads/>`_
  * `pip <https://pip.pypa.io/en/stable/installing/>`_

Getting started
---------------

1. Install package::

    $ pip install doodle-dashboard

2. `Create your dashboard's configuration <https://github.com/SketchingDev/Doodle-Dashboard/wiki/Create-a-dashboard>`_

3. Start the dashboard::

    $ doodledashboard start <PATH TO CONFIGURATION>

Development
-----------

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

