Getting Started
===============

1. Install package::

    pip install doodle-dashboard

2. Start a dashboard:

A dashboard is a YAML file that declares what notifications to show and to what display. Dashboard files can be hosted
locally or remotely.

Starting a single dashboard::

    doodledashboard start \
      https://raw.githubusercontent.com/SketchingDev/Doodle-Dashboard/examples/rss/weather/dashboard.yml

Starting multiple dashboards::

    doodledashboard start \
      https://raw.githubusercontent.com/SketchingDev/Doodle-Dashboard/examples/rss/weather/dashboard.yml \
      https://raw.githubusercontent.com/SketchingDev/Doodle-Dashboard/examples/rss/build-radiator/dashboard.yml


How notifications work
^^^^^^^^^^^^^^^^^^^^^^

.. image:: images/flow-diagram.png