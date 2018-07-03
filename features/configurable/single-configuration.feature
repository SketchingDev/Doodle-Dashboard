Feature: Dashboard is loaded from a configuration file

  Scenario: Dashboard loaded from configuration with only a display
    Given I load test displays
    And I have the configuration called 'config.yml'
      """
      interval: 10
      display: test-display-all-functionality
      """
    When I call 'start --once config.yml'
    Then the status code is 0
    And the output is
      """
      Interval: 10
      Display loaded: test-display-all-functionality
      0 data sources loaded
      0 notifications loaded
      Dashboard running...

      """

  Scenario: Dashboard loaded from configuration with display and notification
    Given I load test displays
    And I have the configuration called 'config.yml'
      """
      interval: 0
      display: test-display-all-functionality
      notifications:
        - title: Dummy Handler
          type: text
      """
    When I call 'start --once config.yml'
    Then the status code is 0
    And the output is
      """
      Interval: 0
      Display loaded: test-display-all-functionality
      0 data sources loaded
      1 notifications loaded
       - Text notification (title=Dummy Handler, text=)
      Dashboard running...
      Displaying Text notification (title=Dummy Handler, text=)

      """