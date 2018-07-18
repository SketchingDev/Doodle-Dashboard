Feature: Dashboard is loaded from a configuration file

  @fixture.server.http
  Scenario: Dashboard loaded from remote URL
    Given I load test displays
    And I have the remote configuration
      """
      display: test-display-all-functionality
      """
    When I call 'start --once %REMOTE_URLS%'
    Then the output is
      """
      Interval: 15
      Display loaded: test-display-all-functionality
      0 data sources loaded
      0 notifications loaded
      Dashboard running...

      """
    And the status code is 0

  @fixture.server.http
  Scenario: Single data-feed with single output represented in JSON
    Given I load test displays
    And I have the remote configuration
      """
      data-feeds:
        - source: text
          text: Test 1
      """
    When I call 'view datafeeds %REMOTE_URLS%'
    Then the output is
      """
      {
          "source-data": [
              {
                  "source": "Text",
                  "text": "Test 1"
              }
          ]
      }

      """
    And the status code is 0