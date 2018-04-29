import logging
import shelve

import click
from yaml import YAMLError

from doodledashboard.configuration.config import DashboardConfigReader, MissingConfigurationValueException
from doodledashboard.configuration.defaultconfig import DefaultConfiguration
from doodledashboard.dashboard_runner import DashboardRunner


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

    _state_storage = shelve.open('/tmp/shelve')

    dashboard_config = DashboardConfigReader()
    DefaultConfiguration.set_creators(_state_storage, dashboard_config)

    dashboard = None
    try:
        dashboard = dashboard_config.read_yaml(config)
        explain_dashboard(dashboard)
    except YAMLError as err:
        click.echo("Error reading YAML in configuration file '%s':\n%s" % (config, err), err=True)
    except MissingConfigurationValueException as err:
        click.echo("Missing value in your configuration:\n%s" % err, err=True)

    if not dashboard:
        raise click.Abort()

    try:
        DashboardRunner(dashboard).run()
    finally:
        _state_storage.close()


cli.add_command(start)


def attach_logging(name):
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    _logger.addHandler(ch)


def explain_dashboard(dashboard):
    interval = dashboard.get_interval()
    click.echo('Interval: %s' % str(interval))

    display = dashboard.get_display()
    click.echo('Display loaded: %s' % str(display))

    data_sources = dashboard.get_data_feeds()
    click.echo('%s data sources loaded' % len(data_sources))
    for data_source in data_sources:
        click.echo(' - %s' % str(data_source))

    notifications = dashboard.get_notifications()
    click.echo('%s notifications loaded' % len(notifications))
    for notification in notifications:
        click.echo(' - %s' % str(notification))


if __name__ == '__main__':
    cli()
