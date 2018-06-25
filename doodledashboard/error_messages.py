from _yaml import ParserError

from doodledashboard.configuration.config import EmptyConfiguration, YamlParsingError, ConfigurationMissingDisplay, \
    NotificationDoesNotSupportDisplay


def get_error_message(error, default=None):
    if not default:
        default = str(error)

    return error_messages.get(error.__class__, lambda err: default)(error)


def empty_configuration(err):
    multiple_configs = len(err.configuration_files) > 1
    if multiple_configs:
        return "All of the configuration files you provided are empty"
    else:
        return "The configuration file you provided is empty"


def error_parsing_yaml(err: YamlParsingError):
    if isinstance(err.parsing_exception, ParserError):
        return "Error %s" % err.parsing_exception

    return "Error parsing configuration file %s due to:\n%s" % (err.config, err.parsing_exception)


def config_missing_display(err):
    return "No display defined. Check that the ID you provided is valid."


def notification_does_not_support_display(err: NotificationDoesNotSupportDisplay):
    missing_requirements = err.get_missing_requirements()

    error_message = "\n".join([" - %s" % r.__name__ for r in missing_requirements])

    return "Display '%s' is missing the following functionality required by the notification '%s':\n%s" % (
        err.display, err.handler, error_message)


error_messages = {
    EmptyConfiguration: empty_configuration,
    YamlParsingError: error_parsing_yaml,
    ConfigurationMissingDisplay: config_missing_display,
    NotificationDoesNotSupportDisplay: notification_does_not_support_display
}
