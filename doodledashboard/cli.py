import click
import json
import logging
import shelve
from yaml import YAMLError

from doodledashboard import __about__
from doodledashboard.configuration.config import DashboardConfigReader, \
    ValidateDashboard, InvalidConfigurationException, ConfigurationMissingDisplay, NotificationDoesNotSupportDisplay
from doodledashboard.configuration.component_loaders import InternalPackageLoader, StaticDisplayLoader, \
    ExternalPackageLoader
from doodledashboard.dashboard_runner import DashboardRunner
from doodledashboard.datafeeds.datafeed import TextEntityJsonEncoder
from doodledashboard.displays.recorddisplay import RecordDisplay
from doodledashboard.error_messages import get_error_message


def attach_logging(ctx, param, value):
    if value:
        _logger = logging.getLogger("doodledashboard")
        _logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        _logger.addHandler(ch)


@click.help_option("-h", "--help")
@click.version_option(__about__.__version__, "-v", "--version", message="%(prog)s v%(version)s")
@click.group()
def cli():
    pass


@cli.command()
@click.argument("configs", type=click.File("rb"), nargs=-1)
@click.option('--once', is_flag=True, help='Whether to run once, otherwise will loop through notifications')
@click.option("--verbose", is_flag=True, callback=attach_logging, expose_value=False)
def start(configs, once):
    """Start dashboard with CONFIG file"""

    with shelve.open("/tmp/shelve") as state_storage:
        dashboard_config = configure_component_loaders(DashboardConfigReader(), state_storage)
        dashboard = read_dashboard_from_config(dashboard_config, configs)

        try:
            ValidateDashboard().validate(dashboard)
        except (NotificationDoesNotSupportDisplay, ConfigurationMissingDisplay) as err:
            click.echo(get_error_message(err, default="Dashboard configuration is invalid"), err=True)
            raise click.Abort()

        explain_dashboard(dashboard)

        click.echo("Dashboard running...")

        while True:
            DashboardRunner(dashboard).cycle()
            if once:
                break


@cli.command()
@click.argument("action", type=click.Choice(["datafeeds", "notifications"]))
@click.argument("configs", type=click.File("rb"), nargs=-1)
def view(action, configs):
    """View what the datafeeds in the CONFIG are returning"""

    dashboard_config = configure_component_loaders(DashboardConfigReader(), {})
    dashboard = read_dashboard_from_config(dashboard_config, configs)

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


def read_dashboard_from_config(dashboard_config, config):
    try:
        return dashboard_config.read_yaml(config)
    except (YAMLError, InvalidConfigurationException) as err:
        click.echo(get_error_message(err, default="Error parsing configuration file"), err=True)
        raise click.Abort()


def configure_component_loaders(dashboard_config, state_storage):
    InternalPackageLoader(state_storage).configure(dashboard_config)
    ExternalPackageLoader().configure(dashboard_config)
    StaticDisplayLoader().configure(dashboard_config)

    return dashboard_config


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
