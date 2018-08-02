Tips for developing displays
============================


Synchronise project files onto embedded device
----------------------------------------------

When developing a plugin for a display for a device like the Raspberry Pi I find it easier to write the code on my
computer and then transfer it across for testing. Given that the device has SSH access you can synchronise project files
using rsync::

    rsync -a . pi@raspberrypi:/home/pi/Doodle-Dashboard-Display-x


Building and install display package locally
--------------------------------------------

Doodle-Dashboard loads displays by
`scanning entry points <https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins>`_
for other packages. If you want to quickly package and install your display locally without publishing remotely you can
use the following commands::

    pip3 uninstall doodle-dashboard-display-x
    python3 setup.py sdist
    pip3 install dist/doodle-dashboard-display-x-0.0.1.tar.gz

