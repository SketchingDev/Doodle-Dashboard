Development
============
1. Clone the repository::

    git clone https://github.com/SketchingDev/Doodle-Dashboard.git
    cd doodle-dashboard

2. Create a development environment

    tox is used to create our project's virtual environment::

        pip3 install tox

        # Creates virtual environments listed in tox.ini
        tox

        # Activates the virtual environment in your shell
        source .tox/py37/bin/activate

    Alternatively you can install the dependencies outside of a virtual environment::

    make dev
    export PYTHONPATH=`pwd`

3. Test that the environment is setup::

    python doodledashboard/cli.py


ImportError: No module named
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you keep getting the ImportError when building the project then check that you
haven't already installed the application via pip, if you have then you might be
pulling in the doodle dashboard classes from your local pip packages instead of
from the project folder.

Remove the library with::

    sudo rm -rf /Library/Python/3.6/site-packages/doodledashboard/

