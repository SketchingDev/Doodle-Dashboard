import logging
import shelve

import click
import yaml

from doodledashboard.configuration.config import DashboardConfig
from doodledashboard.configuration.defaultconfig import DefaultConfiguration
from doodledashboard.dashboard import Dashboard


@click.help_option('-h', '--help')
@click.version_option('0.0.4', '-v', '--version', message='%(prog)s v%(version)s')
@click.group()
def cli():
    pass


@cli.command()
@click.argument('config', type=click.File('rb'))
@click.option('--verbose', is_flag=True)
def start(config, verbose):
    """Start dashboard with CONFIG file"""

    if verbose:
        attach_logging('doodledashboard')

    _config = yaml.load(config)
    _state_storage = shelve.open('/tmp/shelve')

    dashboard_config = DashboardConfig(_config)
    DefaultConfiguration.set_creators(_state_storage, dashboard_config)

    echo_config(dashboard_config)

    _dashboard = Dashboard(
        dashboard_config.get_display(),
        dashboard_config.get_data_feeds(),
        dashboard_config.get_notifications()
    )

    _dashboard.set_update_interval(dashboard_config.get_interval())

    try:
        _dashboard.start()
    finally:
        _state_storage.close()


cli.add_command(start)


def attach_logging(name):
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    _logger.addHandler(ch)


def echo_config(dashboard_config):
    interval = dashboard_config.get_interval()
    click.echo('Interval: %s' % str(interval))

    display = dashboard_config.get_display()
    click.echo('Display loaded: %s' % str(display))

    data_sources = dashboard_config.get_data_feeds()
    click.echo('%s data sources loaded' % len(data_sources))
    for data_source in data_sources:
        click.echo(' - %s' % str(data_source))

    notifications = dashboard_config.get_notifications()
    click.echo('%s notifications loaded' % len(notifications))
    for notification in notifications:
        click.echo(' - %s' % str(notification))


if __name__ == '__main__':
    cli()
