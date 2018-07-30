from doodledashboard.configuration.config import EmptyConfiguration, YamlParsingError, DisplayNotFound, \
    DisplayDoesNotSupportNotification


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


def error_parsing_yaml(err):
    if hasattr(err, "parsing_exception"):
        return "Error %s" % err.parsing_exception

    return "Error parsing configuration file %s due to:\n%s" % (err.config, err.parsing_exception)


def display_not_found(err):
    return "Cannot find the display '%s'. Have you run `pip install` for the display you're trying to use?" \
           % err.display_id


def display_does_not_support_notification(err: DisplayDoesNotSupportNotification):
    supported_notifications = err.display.get_supported_notifications()
    if len(supported_notifications) > 0:
        notification_list = "\n".join([" - %s" % n.__name__ for n in supported_notifications])

        return "Display '%s' does not support the notification '%s'. " \
               "The notifications this display does support are:\n%s" % \
               (err.display, err.notification, notification_list)

    return "Display '%s' does not support any notifications, which is very odd..." % err.display


error_messages = {
    EmptyConfiguration: empty_configuration,
    YamlParsingError: error_parsing_yaml,
    DisplayNotFound: display_not_found,
    DisplayDoesNotSupportNotification: display_does_not_support_notification
}
