import click
import json
import logging
import shelve
from yaml import YAMLError

from doodledashboard import __about__
from doodledashboard.configuration.config import DashboardConfigReader, \
    ValidateDashboard, InvalidConfigurationException
from doodledashboard.configuration.component_loaders import AllInPackageLoader, StaticDisplayLoader
from doodledashboard.dashboard_runner import DashboardRunner
from doodledashboard.datafeeds.datafeed import TextEntityJsonEncoder
from doodledashboard.displays.recorddisplay import RecordDisplay


@click.help_option("-h", "--help")
@click.version_option(__about__.__version__, "-v", "--version", message="%(prog)s v%(version)s")
@click.group()
def cli():
    pass


@cli.command()
@click.argument("config", type=click.File("rb"))
@click.option('--once', is_flag=True, help='Whether to run once, otherwise will loop through notifications')
@click.option("--verbose", is_flag=True)
def start(config, once, verbose):
    """Start dashboard with CONFIG file"""

    if verbose:
        attach_logging("doodledashboard")

    with shelve.open("/tmp/shelve") as state_storage:

        dashboard_config = DashboardConfigReader()

        AllInPackageLoader(state_storage).configure(dashboard_config)
        StaticDisplayLoader().configure(dashboard_config)

        dashboard = try_read_dashboard_config(dashboard_config, config)

        try:
            ValidateDashboard().validate(dashboard)
        except InvalidConfigurationException as err:
            click.echo("Error reading configuration file '%s':\n%s" % (config.name, err.value), err=True)
            raise click.Abort()

        explain_dashboard(dashboard)

        click.echo("Dashboard running...")

        while True:
            DashboardRunner(dashboard).cycle()
            if once:
                break


@cli.command()
@click.argument("action", type=click.Choice(["datafeeds", "notifications"]))
@click.argument("config", type=click.File("rb"))
def view(action, config):
    """View what the datafeeds in the CONFIG are returning"""

    dashboard_config = DashboardConfigReader()

    AllInPackageLoader({}).configure(dashboard_config)
    StaticDisplayLoader().configure(dashboard_config)

    dashboard = try_read_dashboard_config(dashboard_config, config)

    datafeed_responses = DashboardRunner(dashboard).poll_datafeeds()

    output = {"source-data": datafeed_responses}
    if action == "notifications":
        notifications_output = []
        for notification in dashboard.get_notifications():
            filtered_responses = notification.filter(datafeed_responses)

            display = RecordDisplay()
            notification.process(datafeed_responses)
            notification.draw(display)

            notifications_output.append(
                {
                    "name": str(notification),
                    "filtered-data": filtered_responses,
                    "handler-actions": display.get_calls()
                }
            )

        output["notifications"] = notifications_output

    click.echo(json.dumps(output, sort_keys=True, indent=4, cls=TextEntityJsonEncoder))


def try_read_dashboard_config(dashboard_config, config):
    try:
        return dashboard_config.read_yaml(config)
    except YAMLError as err:
        click.echo("Error parsing configuration file '%s':\n%s" % (config.name, err), err=True)
    except InvalidConfigurationException as err:
        click.echo("Error reading configuration file '%s':\n%s" % (config.name, err.value), err=True)

    raise click.Abort()


def attach_logging(name):
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    _logger.addHandler(ch)


def explain_dashboard(dashboard):
    interval = dashboard.get_interval()
    click.echo("Interval: %s" % str(interval))

    display = dashboard.get_display()
    click.echo("Display loaded: %s" % str(display))

    data_sources = dashboard.get_data_feeds()
    click.echo("%s data sources loaded" % len(data_sources))
    for data_source in data_sources:
        click.echo(" - %s" % str(data_source))

    notifications = dashboard.get_notifications()
    click.echo("%s notifications loaded" % len(notifications))
    for notification in notifications:
        click.echo(" - %s" % str(notification))


if __name__ == "__main__":
    cli()
