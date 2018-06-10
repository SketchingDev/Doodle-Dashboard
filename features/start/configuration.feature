Feature: Configuration is printed to output


  Scenario: Emtpy configuration causes error
    Given I have the configuration
      """
      """
    When I call 'start --once config.yml'
    Then the status code is 1
    And the output is
      """
      Error reading configuration file 'config.yml':
      'Configuration file is empty'
      Aborted!

      """

  Scenario: Malformed YAML configuration causes error
    Given I have the configuration
      """
      :
      """
    When I call 'start --once config.yml'
    Then the status code is 1
    And the output is
      """
      Error parsing configuration file 'config.yml':
      while parsing a block mapping
      expected <block end>, but found ':'
        in "config.yml", line 1, column 1
      Aborted!

      """

  Scenario: Invalid data-feed causes error
    Given I have the configuration
       """
       data-feeds: testing
       """
    When I call 'start --once config.yml'
    Then the status code is 1
    And the output is
       """
       Error reading configuration file 'config.yml':
       'No display defined. Check that the ID you provided is valid.'
       Aborted!

       """

  Scenario: Config printed showing no data-feeds nor handlers
    Given I have the configuration
       """
       interval: 10
       display: console
       """
    When I call 'start --once config.yml'
    Then the status code is 0
    And the output is
       """
       Interval: 10
       Display loaded: Console display
       0 data sources loaded
       0 notifications loaded
       Dashboard running...

       """

  Scenario: Config printed showing one notification
    Given I have the configuration
       """
       interval: 0
       display: console
       notifications:
         - title: Dummy Handler
           handler: text-handler
       """
    When I call 'start --once config.yml'
    Then the status code is 0
    And the output is
       """
       Interval: 0
       Display loaded: Console display
       0 data sources loaded
       1 notifications loaded
        - Displays entities using: Text handler
       Dashboard running...


       """
