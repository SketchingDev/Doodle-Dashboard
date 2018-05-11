import json
import logging
import shelve

import click
from yaml import YAMLError

from doodledashboard.configuration.config import DashboardConfigReader, MissingConfigurationValueException
from doodledashboard.configuration.defaultconfig import FullConfigCollection, DatafeedConfigCollection
from doodledashboard.dashboard_runner import DashboardRunner
from doodledashboard.datafeeds.repository import MessageModelEncoder


@click.help_option("-h", "--help")
@click.version_option("0.0.4", "-v", "--version", message="%(prog)s v%(version)s")
@click.group()
def cli():
    pass


@cli.command()
@click.argument("config", type=click.File("rb"))
@click.option("--verbose", is_flag=True)
def start(config, verbose):
    """Start dashboard with CONFIG file"""

    if verbose:
        attach_logging("doodledashboard")

    with shelve.open("/tmp/shelve") as state_storage:

        dashboard_config = DashboardConfigReader(FullConfigCollection(state_storage))
        dashboard = try_read_dashboard_config(dashboard_config, config)

        explain_dashboard(dashboard)
        DashboardRunner(dashboard).run()


@cli.command()
@click.argument("type", type=click.Choice(["datafeeds"]))
@click.argument("config", type=click.File("rb"))
def view(type, config):
    """View what the datafeeds in the CONFIG are returning"""

    dashboard_config = DashboardConfigReader(DatafeedConfigCollection())
    dashboard = try_read_dashboard_config(dashboard_config, config)

    datafeed_responses = [feed.get_latest_messages() for feed in dashboard.get_data_feeds()]
    click.echo(json.dumps(datafeed_responses, sort_keys=True, indent=4, cls=MessageModelEncoder))


def try_read_dashboard_config(dashboard_config, config):
    try:
        return dashboard_config.read_yaml(config)
    except YAMLError as err:
        click.echo(f"Error reading YAML in configuration file '{config.name}':\n{err}", err=True)
    except MissingConfigurationValueException as err:
        click.echo(f"Missing value in your configuration:\n{err}", err=True)

    raise click.Abort()


def attach_logging(name):
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    _logger.addHandler(ch)


def explain_dashboard(dashboard):
    interval = dashboard.get_interval()
    click.echo(f"Interval: {str(interval)}")

    display = dashboard.get_display()
    click.echo(f"Display loaded: {str(display)}")

    data_sources = dashboard.get_data_feeds()
    click.echo(f"{len(data_sources)} data sources loaded")
    for data_source in data_sources:
        click.echo(f" - {str(data_source)}")

    notifications = dashboard.get_notifications()
    click.echo(f"{len(notifications)} notifications loaded")
    for notification in notifications:
        click.echo(f" - {str(notification)}")


if __name__ == "__main__":
    cli()
