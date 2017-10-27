import sys

from dashboards import StandardDashboard
from doodledashboard.lucas.displays.display import LoggingDisplay
from lucas.client import SlackConfig
from lucas.factories import DashboardLogger

import shelve

if __name__ == '__main__':
    _shelve = shelve.open('/tmp/shelve')
    _logger = DashboardLogger().register()
    _slack_config = SlackConfig.create_from_file(sys.argv[1])

    _display = LoggingDisplay()
    _dashboard = StandardDashboard(_slack_config, _display, _shelve)

    try:
        _dashboard.start()
    except KeyboardInterrupt:
        _shelve.close()
        sys.exit(0)
    except ValueError as err:
        _shelve.close()
        _logger.critical(err)
        sys.exit(1)
