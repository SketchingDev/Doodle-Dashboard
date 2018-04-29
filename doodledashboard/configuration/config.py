from doodledashboard.dashboard import Notification


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


class DashboardConfig:
    _FIVE_SECONDS = 5

    def __init__(self, config):
        self._config = config
        self._filter_creator = None
        self._handler_creator = None
        self._data_source_creator = None
        self._display_creator = None

    def set_filter_creators(self, filter_creator):
        self._filter_creator = filter_creator

    def set_handler_creators(self, handler_creator):
        self._handler_creator = handler_creator

    def set_data_source_creators(self, data_source_creator):
        self._data_source_creator = data_source_creator

    def set_display_creator(self, display_creator):
        self._display_creator = display_creator

    def get_interval(self):
        if 'interval' in self._config:
            return self._config['interval']
        else:
            return DashboardConfig._FIVE_SECONDS

    def get_display(self):
        # TODO: Fix issue with circular dependency that I get when this import is moved to the top
        # https://stackoverflow.com/questions/9252543/importerror-cannot-import-name-x
        from doodledashboard.displays.loggingdecorator import LoggingDisplayDecorator

        display = self._display_creator.create(self._config)
        if not display:
            raise MissingConfigurationValueException('Missing display option')

        return LoggingDisplayDecorator(display)

    def get_data_feeds(self):
        data_source_elements = []
        # DataSourceConfigSection
        if 'data-feeds' in self._config:
            data_source_elements = self._config['data-feeds']

        return self._create_items(self._data_source_creator, data_source_elements)

    def get_notifications(self):
        notifications = []

        # NotificationsConfigSection
        if 'notifications' in self._config:
            for notification_element in self._config['notifications']:

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

        if not self._filter_creator:
            return root_filter

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
