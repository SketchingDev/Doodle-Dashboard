import click
import json
import logging

from doodledashboard import __about__
from doodledashboard.configuration.component_loaders import InternalPackageLoader, \
    ExternalPackageLoader, CreatorsContainer, StaticDisplayLoader
from doodledashboard.configuration.config import DashboardConfigReader, \
    ValidateDashboard, InvalidConfigurationException
from doodledashboard.dashboard_runner import DashboardRunner
from doodledashboard.datafeeds.datafeed import MessageJsonEncoder
from doodledashboard.error_messages import get_error_message
from doodledashboard.filters.record_filter import RecordFilter


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

    dashboard_config = DashboardConfigReader(collect_component_creators())

    default_configuration = [
        """
        interval: 15
        display: console
        """
    ]
    default_configuration += configs
    dashboard = read_dashboard_from_config(dashboard_config, default_configuration)

    try:
        ValidateDashboard().validate(dashboard)
    except Exception as err:
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

    dashboard_config = DashboardConfigReader(collect_component_creators())

    dashboard = read_dashboard_from_config(dashboard_config, configs)
    messages = DashboardRunner(dashboard).poll_datafeeds()

    output = {"source-data": messages}

    if action == "notifications":
        output["notifications"] = []

        for notification in dashboard.get_notifications():
            notification_before = str(notification)

            updater = notification.get_updater()
            record_filter = RecordFilter()
            if updater:
                updater.add_message_filters([record_filter])

            for message in messages:
                notification.update(message)

            output["notifications"].append({
                "filtered-messages": messages if not updater else record_filter.get_messages(),
                "notification-before": notification_before,
                "notification-after": str(notification)
            })

    click.echo(json.dumps(output, sort_keys=True, indent=4, cls=MessageJsonEncoder))


@cli.command()
@click.argument("action", type=click.Choice(["displays", "datafeeds", "notifications", "all"]), default="all")
def list(action):
    """View what the datafeeds in the CONFIG are returning"""
    creator_container = collect_component_creators()
    if action == "datafeeds" or action == "all":
        datafeed_ids = {c.id_key_value[1] for c in creator_container.get_data_feed_creators()}

        click.echo("Available data-feeds:")
        for datafeed_id in sorted(datafeed_ids):
            click.echo(" - %s" % datafeed_id)

    if action == "all":
        click.echo("")

    if action == "displays" or action == "all":
        display_ids = {c.id_key_value[1] for c in creator_container.get_display_creators()}

        click.echo("Available displays:")
        for display_id in sorted(display_ids):
            click.echo(" - %s" % display_id)


def read_dashboard_from_config(dashboard_config, configs):
    try:
        return dashboard_config.read_yaml(configs)
    except InvalidConfigurationException as err:
        click.echo(get_error_message(err, default="Error parsing configuration file"), err=True)
        raise click.Abort()


def collect_component_creators():
    container = CreatorsContainer()
    InternalPackageLoader().populate(container)
    ExternalPackageLoader().populate(container)
    StaticDisplayLoader().populate(container)

    return container


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
