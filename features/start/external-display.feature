Feature: Configuration loads external displays

    Scenario: Config printed showing display added to static loader
      Given I load test displays
      And I have the configuration called 'config.yml'
         """
         interval: 0
         display: test-display-no-functionality
         """
      When I call 'start --once config.yml'
      Then the status code is 0
      And the output is
         """
         Interval: 0
         Display loaded: test-display-no-functionality
         0 data sources loaded
         0 notifications loaded
         Dashboard running...

         """

    Scenario: Display without functionality required by notification causes error
      Given I load test displays
      And I have the configuration called 'config.yml'
         """
         interval: 0
         display: test-display-no-functionality
         notifications:
         - title: Dummy Handler
           handler: text-handler
         """
      When I call 'start --once config.yml'
      Then the status code is 1
      And the output is
         """
         Display 'test-display-no-functionality' is missing the following functionality required by the notification 'Text handler':
          - CanWriteText
         Aborted!

         """