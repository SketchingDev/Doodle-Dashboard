Feature: Notification prints to output derived from data-feeds

  Scenario: Config printed showing one notification
    Given I have the configuration
       """
       interval: 0
       display: console
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
       Display loaded: Console display
       2 data sources loaded
        - Text
        - Text
       1 notifications loaded
        - Displays entities using: Text handler
       Dashboard running...
       Test 3

       """
