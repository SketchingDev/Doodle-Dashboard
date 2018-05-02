import yaml

from doodledashboard.dashboard_runner import Notification, Dashboard


class Creator:
    def __init__(self):
        self._successor = None

    def can_create(self, config_section):
        raise NotImplementedError('Implement this method')

    def create_item(self, config_section):
        raise NotImplementedError('Implement this method')

    def add(self, successor):
        if not self._successor:
            self._successor = successor
        else:
            self._successor.add(successor)

    def create(self, config_section):
        if self.can_create(config_section):
            return self.create_item(config_section)
        elif self._successor:
            return self._successor.create(config_section)
        else:
            return None


class RootCreator(Creator):

    def can_create(self, config_section):
        return False

    def create_item(self, config_section):
        pass


class FilterConfigCreator(Creator):
    def __init__(self):
        Creator.__init__(self)

    def creates_for_id(self, filter_id):
        raise NotImplementedError('Implement this method')

    def can_create(self, config_section):
        return 'type' in config_section and self.creates_for_id(config_section['type'])

    def create_item(self, config_section):
        raise NotImplementedError('Implement this method')


class MissingRequiredOptionException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DashboardConfigReader:
    _FIVE_SECONDS = 5

    def __init__(self, config_creators=None):
        self._filter_creator = RootCreator()
        self._handler_creator = RootCreator()
        self._data_feed_creator = RootCreator()
        self._display_creator = RootCreator()

        if config_creators:
            config_creators.configure(self)

    def add_filter_creators(self, creators):
        self._add_creator_to_chain(self._filter_creator, creators)

    def add_handler_creators(self, creators):
        self._add_creator_to_chain(self._handler_creator, creators)

    def add_data_source_creators(self, creators):
        self._add_creator_to_chain(self._data_feed_creator, creators)

    def add_display_creators(self, creators):
        self._add_creator_to_chain(self._display_creator, creators)

    @staticmethod
    def _add_creator_to_chain(chain, creators):
        for creator in creators:
            chain.add(creator)

    def read_yaml(self, config_yaml):
        config = yaml.safe_load(config_yaml)

        return Dashboard(
            self._extract_interval(config),
            self._extract_display(config),
            self._extract_data_feeds(config),
            self._extract_notifications(config)
        )

    def _extract_interval(self, config):
        if 'interval' in config:
            return config['interval']
        else:
            return DashboardConfigReader._FIVE_SECONDS

    def _extract_display(self, config):
        # TODO: Fix issue with circular dependency that I get when this import is moved to the top
        # https://stackoverflow.com/questions/9252543/importerror-cannot-import-name-x
        from doodledashboard.displays.loggingdecorator import LoggingDisplayDecorator

        display = self._display_creator.create(config)
        # if not display:
        #     raise MissingConfigurationValueException('Missing display option')
        if display:
            return LoggingDisplayDecorator(display)
        else:
            return None

    def _extract_data_feeds(self, config):
        data_source_elements = []
        # DataSourceConfigSection
        if 'data-feeds' in config:
            data_source_elements = config['data-feeds']

        return self._create_items(self._data_feed_creator, data_source_elements)

    def _extract_notifications(self, config):
        notifications = []

        # NotificationsConfigSection
        if 'notifications' in config:
            for notification_element in config['notifications']:

                handler = self._handler_creator.create(notification_element)
                if handler:
                    notification = Notification(handler)

                    filter_chain = self._extract_from_filter_chain(notification_element)
                    if filter_chain:
                        notification.set_filter_chain(filter_chain)

                    notifications.append(notification)

        return notifications

    def _extract_from_filter_chain(self, notification_element):
        # TODO: Fix issue with circular dependency that I get when this import is moved to the top
        # https://stackoverflow.com/questions/9252543/importerror-cannot-import-name-x
        from doodledashboard.filters import MessageFilter

        root_filter = MessageFilter()

        # FilterChainConfigSection
        if 'filter-chain' in notification_element:
            filter_chain_elements = notification_element['filter-chain']

            for filter_element in filter_chain_elements:
                new_filter = self._filter_creator.create(filter_element)
                if new_filter:
                    root_filter.add(new_filter)

        return root_filter

    @staticmethod
    def _create_items(creator_chain, config_elements):
        creation = []
        for element in config_elements:
            repository = creator_chain.create(element)
            if repository:
                creation.append(repository)

        return creation


class MissingConfigurationValueException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
