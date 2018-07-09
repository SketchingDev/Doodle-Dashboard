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

  Scenario: Last config takes precedence
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
      Interval: 999
      Display loaded: test-display-all-functionality
      0 data sources loaded
      0 notifications loaded
      Dashboard running...

      """

  Scenario: Data-feed in each configuration
    Given I load test displays
    And I have the configuration called 'config1.yml'
      """
      interval: 1
      display: test-display-all-functionality
      data-feeds:
        - source: text
          text: Test 1
      """
    And I have the configuration called 'config2.yml'
      """
      data-feeds:
        - source: text
          text:
          text: Test 2
      """
    When I call 'start --once config1.yml config2.yml'
    Then the output is
      """
      Interval: 1
      Display loaded: test-display-all-functionality
      2 data sources loaded
       - Text
       - Text
      0 notifications loaded
      Dashboard running...

      """

  Scenario: Notification in each configuration
    Given I load test displays
    And I have the configuration called 'config1.yml'
      """
      interval: 1
      display: test-display-all-functionality
      notifications:
        - title: Test 1
          type: text
      """
    And I have the configuration called 'config2.yml'
      """
      notifications:
        - title: Test 2
          type: text
      """
    When I call 'start --once config1.yml config2.yml'
    Then the output is
      """
      Interval: 1
      Display loaded: test-display-all-functionality
      0 data sources loaded
      2 notifications loaded
       - Text notification (title=Test 1, text=)
       - Text notification (title=Test 2, text=)
      Dashboard running...
      Displaying Text notification (title=Test 1, text=)
      Displaying Text notification (title=Test 2, text=)

      """