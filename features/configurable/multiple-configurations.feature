Feature: Dashboard is loaded from multiple configuration files

  Scenario: Dashboard loaded from multiple configurations
    Given I load test displays
    And I have the configuration called 'config1.yml'
      """
      interval: 123
      """
    And I have the configuration called 'config2.yml'
      """
      display: test-display-all-functionality
      """
    When I call 'start --once config1.yml config2.yml'
    Then the output is
      """
      Interval: 123
      Display loaded: test-display-all-functionality
      0 data sources loaded
      0 notifications loaded
      Dashboard running...

      """

  Scenario: Dashboard loaded from multiple configurations with first config taking precedence
    Given I load test displays
    And I have the configuration called 'config1.yml'
      """
      interval: 123
      """
    And I have the configuration called 'config2.yml'
      """
      interval: 999
      display: test-display-all-functionality
      """
    When I call 'start --once config1.yml config2.yml'
    Then the output is
      """
      Interval: 123
      Display loaded: test-display-all-functionality
      0 data sources loaded
      0 notifications loaded
      Dashboard running...

      """
