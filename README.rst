Doodle-Dashboard: Simple dashboards for all!
============================================

.. image:: https://img.shields.io/pypi/v/doodle-dashboard.svg
    :target: https://pypi.org/project/doodle-dashboard/

.. image:: https://travis-ci.org/SketchingDev/Doodle-Dashboard.svg?branch=master
    :target: https://travis-ci.org/SketchingDev/Doodle-Dashboard

---------------

**Doodle-Dashboard** is used to create fun little dashboards that display useful information from multiple sources, like
Tweets from your favourite Twitterers, weather reports for your local area or breaking news.

.. image:: https://raw.githubusercontent.com/SketchingDev/Doodle-Dashboard/master/docs/images/flow-diagram.png

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

    $ doodledashboard <ABSOLUTE PATH TO YAML CONFIGURATION>

Development
-----------

1. Clone the repository::

    $ git clone https://github.com/SketchingDev/Doodle-Dashboard.git
    $ cd doodle-dashboard

2. Install project dependencies::

    $ make dev

3. See help::

    $ export PYTHONPATH=`pwd`
    $ python doodledashboard/cli.py

ImportError: No module named
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you keep getting the ImportError when building the project check that you
haven't already installed the application via pip, otherwise you might be pulling
in the doodle dashboard classes from your local pip packages.

Remove the library with::

    $ sudo rm -rf /Library/Python/3.6/site-packages/doodledashboard/
