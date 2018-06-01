Feature: View output of data-feeds

    Scenario: Emtpy configuration causes error
     Given I have the configuration
        """
        """
     When I call 'view notifications config.yml'
     Then the status code is 1
     And the output is
        """
        Configuration file is empty
        Aborted!

        """

  Scenario: No notifications represented in JSON
    Given I have the configuration
       """
       notifications:
       """
    When I call 'view notifications config.yml'
    Then the status code is 0
    And the output is
       """
       {
           "notifications": [],
           "source-data": []
       }

       """

  Scenario: Single notification that writes Hello to the display in JSON
    Given I have the configuration
       """
       data-feeds:
         - source: text
           text:
            - Hello
            - Bob
         - source: text
           text: World
       notifications:
         - title: Display weather
           handler: text-handler
           filter-chain:
             - type: message-matches-regex
               pattern: (Hello)
       """
    When I call 'view notifications config.yml'
    Then the status code is 0
    And the output is
       """
       {
           "notifications": [
               {
                   "filtered-data": [
                       {
                           "source": "Text",
                           "text": "Hello"
                       }
                   ],
                   "handler-actions": [
                       "Write text: 'Hello'"
                   ],
                   "name": "Displays entities using: Text handler"
               }
           ],
           "source-data": [
               {
                   "source": "Text",
                   "text": "Hello"
               },
               {
                   "source": "Text",
                   "text": "Bob"
               },
               {
                   "source": "Text",
                   "text": "World"
               }
           ]
       }

       """