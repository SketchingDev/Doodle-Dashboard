Feature: List components

  Scenario: List command lists all loaded data-feeds
   When I call 'list datafeeds'
   Then the status code is 0
   And the output is
     """
     Available datafeeds:
      - datetime
      - rss
      - slack
      - text

     """

  Scenario: List command lists all loaded displays
   Given I load test displays
   When I call 'list displays'
   Then the status code is 0
   And the output is
     """
     Available displays:
      - console
      - test-display-all-functionality
      - test-display-no-functionality

     """

  Scenario: List command lists all loaded filters
   Given I load test displays
   When I call 'list filters'
   Then the status code is 0
   And the output is
     """
     Available filters:
      - message-contains-text
      - message-matches-regex

     """

  Scenario: List command lists all loaded notifications
   Given I load test displays
   When I call 'list notifications'
   Then the status code is 0
   And the output is
     """
     Available notifications:
      - colour
      - image
      - image-with-text
      - text

     """

  Scenario: List command lists all loaded updaters
   Given I load test displays
   When I call 'list updaters'
   Then the status code is 0
   And the output is
     """
     Available updaters:
      - image-depending-on-message-content
      - text-from-message

     """

  Scenario: List command lists all loaded components
   Given I load test displays
   When I call 'list all'
   Then the status code is 0
   And the output is
     """
     Available datafeeds:
      - datetime
      - rss
      - slack
      - text

     Available displays:
      - console
      - test-display-all-functionality
      - test-display-no-functionality

     Available filters:
      - message-contains-text
      - message-matches-regex

     Available notifications:
      - colour
      - image
      - image-with-text
      - text

     Available updaters:
      - image-depending-on-message-content
      - text-from-message


     """

  Scenario: List command shows help is incorrect option
   Given I load test displays
   When I call 'list test'
   Then the status code is 2
   And the output is
     """
     Usage: list [OPTIONS] [COMPONENT_TYPE]

     Error: Invalid value for "component_type": invalid choice: test. (choose from displays, datafeeds, filters, notifications, updaters, all)

     """