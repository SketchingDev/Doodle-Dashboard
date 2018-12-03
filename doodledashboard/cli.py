import click
import json
import logging
import os
import re
from yaml import YAMLError

from doodledashboard import __about__
from doodledashboard.component import ExternalPackageSource, StaticComponentSource, ComponentConfigLoader, ComponentType
from doodledashboard.configuration import DashboardConfigReader, InvalidConfigurationException
from doodledashboard.dashboard import DashboardRunner, DashboardValidator, ValidationException
from doodledashboard.datafeeds.datafeed import MessageJsonEncoder
from doodledashboard.error_messages import get_error_message
from doodledashboard.notifications.notification import FilteredNotification
from doodledashboard.secrets_store import InvalidSecretsException, try_read_secrets_file, SecretNotFound


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
        with open(config_file, 'r') as f:
            return f.read()


@cli.command()
@click.argument("dashboards", type=click.Path(), nargs=-1)
@click.option('--once', is_flag=True, help='Loop through notifications once, otherwise will loop indefinitely')
@click.option("--secrets", type=click.Path(exists=True))
@click.option("--verbose", is_flag=True, callback=attach_logging, expose_value=False)
def start(dashboards, once, secrets):
    """Display a dashboard from the dashboard file(s) provided in the DASHBOARDS
       Paths and/or URLs for dashboards (URLs must secrets with http or https)
    """

    if secrets is None:
        secrets = os.path.join(os.path.expanduser("~"), "/.doodledashboard/secrets")

    try:
        loaded_secrets = try_read_secrets_file(secrets)
    except InvalidSecretsException as err:
        click.echo(get_error_message(err, default="Secrets file is invalid"), err=True)
        raise click.Abort()

    read_configs = ["""
    dashboard:
      display:
        type: console
    """]
    for dashboard_file in dashboards:
        read_configs.append(read_file(dashboard_file))

    dashboard_config = DashboardConfigReader(initialise_component_loader(), loaded_secrets)

    try:
        dashboard = read_dashboard_from_config(dashboard_config, read_configs)
    except YAMLError as err:
        click.echo(get_error_message(err, default="Dashboard configuration is invalid"), err=True)
        raise click.Abort()

    try:
        DashboardValidator().validate(dashboard)
    except ValidationException as err:
        click.echo(get_error_message(err, default="Dashboard configuration is invalid"), err=True)
        raise click.Abort()

    explain_dashboard(dashboard)

    click.echo("Dashboard running...")

    while True:
        try:
            DashboardRunner(dashboard).cycle()
        except SecretNotFound as err:
            click.echo(get_error_message(err, default="Datafeed didn't have required secret"), err=True)
            raise click.Abort()

        if once:
            break


@cli.command()
@click.argument("action", type=click.Choice(["datafeeds", "notifications"]))
@click.argument("dashboards", type=click.Path(), nargs=-1)
@click.option("--secrets", type=click.Path(exists=True))
@click.option("--verbose", is_flag=True, callback=attach_logging, expose_value=False)
def view(action, dashboards, secrets):
    """View the output of the datafeeds and/or notifications used in your DASHBOARDS"""

    if secrets is None:
        secrets = os.path.join(os.path.expanduser("~"), "/.doodledashboard/secrets")

    try:
        loaded_secrets = try_read_secrets_file(secrets)
    except InvalidSecretsException as err:
        click.echo(get_error_message(err, default="Secrets file is invalid"), err=True)
        raise click.Abort()

    dashboard_config = DashboardConfigReader(initialise_component_loader(), loaded_secrets)

    read_configs = [read_file(f) for f in dashboards]
    dashboard = read_dashboard_from_config(dashboard_config, read_configs)

    try:
        messages = DashboardRunner(dashboard).poll_datafeeds()
    except SecretNotFound as err:
        click.echo(get_error_message(err, default="Datafeed didn't have required secret"), err=True)
        raise click.Abort()

    cli_output = {"source-data": messages}

    if action == "notifications":
        cli_output["notifications"] = []

        for notification in dashboard.notifications:
            notification_output = notification.create(messages)

            filtered_messages = messages

            if isinstance(notification, FilteredNotification):
                filtered_messages = notification.filter_messages(messages)

            cli_output["notifications"].append({
                "filtered-messages": filtered_messages,
                "notification": str(notification_output)
            })
    json_output = json.dumps(cli_output, sort_keys=True, indent=4, cls=MessageJsonEncoder)
    click.echo(json_output)


@cli.command()
@click.argument("component_type",
                type=click.Choice(["displays", "datafeeds", "filters", "notifications", "all"]),
                default="all")
def list(component_type):
    """List components that are available on your machine"""
    config_loader = initialise_component_loader()
    component_types = sorted({
         "displays": lambda: config_loader.load_by_type(ComponentType.DISPLAY),
         "datafeeds": lambda: config_loader.load_by_type(ComponentType.DATA_FEED),
         "filters": lambda: config_loader.load_by_type(ComponentType.FILTER),
         "notifications": lambda: config_loader.load_by_type(ComponentType.NOTIFICATION)
    }.items(), key=lambda t: t[0])

    def print_ids(creators):
        ids = {c.id_key_value[1] if hasattr(c, "id_key_value") else c.get_id() for c in creators}
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
    except Exception:
        raise


def initialise_component_loader():
    configs = ComponentConfigLoader()
    configs.add_source(ExternalPackageSource())
    configs.add_source(StaticComponentSource())
    return configs


def explain_dashboard(dashboard):
    display = dashboard.display
    click.echo("Display loaded: %s" % str(display))

    data_sources = dashboard.data_feeds
    click.echo("%s data sources loaded" % len(data_sources))
    for data_source in data_sources:
        click.echo(" - %s" % str(data_source))

    notifications = dashboard.notifications
    click.echo("%s notifications loaded" % len(notifications))
    for notification in notifications:
        click.echo(" - %s" % str(notification))


if __name__ == "__main__":
    cli()
