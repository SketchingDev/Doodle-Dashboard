import click
import json
import logging
import re

from doodledashboard import __about__
from doodledashboard.configuration.component_loaders import ExternalPackageLoader, CreatorsContainer, \
    StaticDisplayLoader
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


def is_remote_file(file_path):
    regex = re.compile("^(http|https)://", re.IGNORECASE)
    return True if regex.search(file_path) else False


def read_remote_file(file_path):
    import urllib.request
    with urllib.request.urlopen(file_path) as response:
        return response.read()


def read_file(config_file):
    if is_remote_file(config_file):
        return read_remote_file(config_file)
    else:
        return open(config_file, 'r')


@cli.command()
@click.argument("dashboards", type=click.Path(), nargs=-1)
@click.option('--once', is_flag=True, help='Loop through notifications once, otherwise will loop indefinitely')
@click.option("--verbose", is_flag=True, callback=attach_logging, expose_value=False)
def start(dashboards, once):
    """Display a dashboard from the dashboard file(s) provided in the DASHBOARDS
       Paths and/or URLs for dashboards (URLs must start with http or https)
    """

    default_configuration = """
        interval: 15
        display: console
        """

    read_configs = [default_configuration]
    for dashboard_file in dashboards:
        read_configs.append(read_file(dashboard_file))

    dashboard_config = DashboardConfigReader(collect_component_creators())

    dashboard = read_dashboard_from_config(dashboard_config, read_configs)

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
@click.argument("dashboards", type=click.Path(), nargs=-1)
def view(action, dashboards):
    """View what the datafeeds in the DASHBOARDS are returning"""

    dashboard_config = DashboardConfigReader(collect_component_creators())

    read_configs = [read_file(f) for f in dashboards]
    dashboard = read_dashboard_from_config(dashboard_config, read_configs)

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
@click.argument("component_type",
                type=click.Choice(["displays", "datafeeds", "filters", "notifications", "updaters", "all"]),
                default="all")
def list(component_type):

    creator_container = collect_component_creators()
    component_types = sorted({
        "displays": lambda: creator_container.get_display_creators(),
        "datafeeds": lambda: creator_container.get_data_feed_creators(),
        "filters": lambda: creator_container.get_filter_creators(),
        "notifications": lambda: creator_container.get_notification_creators(),
        "updaters": lambda: creator_container.get_notification_updater_creators()
    }.items(), key=lambda t: t[0])

    def print_ids(creators):
        ids = {c.id_key_value[1] for c in creators}
        for i in sorted(ids):
            click.echo(" - %s" % i)

    for k, v in component_types:
        if component_type == k or component_type == "all":
            click.echo("Available %s:" % k)
            print_ids(v())

        if component_type == "all":
            click.echo("")


def read_dashboard_from_config(dashboard_config, configs):
    try:
        return dashboard_config.read_yaml(configs)
    except InvalidConfigurationException as err:
        click.echo(get_error_message(err, default="Error parsing configuration file"), err=True)
        raise click.Abort()


def collect_component_creators():
    container = CreatorsContainer()
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
