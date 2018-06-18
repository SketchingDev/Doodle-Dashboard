Feature: Notification prints to output derived from data-feeds

  Scenario: Config printed showing one notification
    Given I load test displays
    And I have the configuration called 'config.yml'
       """
       interval: 0
       display: test-display-all-functionality
       data-feeds:
         - source: text
           text: Test 1
         - source: text
           text:
             - Test 2
             - Test 3
       notifications:
         - title: Dummy Handler
           handler: text-handler
       """
    When I call 'start --once config.yml'
    Then the status code is 0
    And the output is
       """
       Interval: 0
       Display loaded: test-display-all-functionality
       2 data sources loaded
        - Text
        - Text
       1 notifications loaded
        - Displays entities using: Text handler
       Dashboard running...
       Clear display
       Write text: 'Test 3'

       """
