Feature: View output of data-feeds

    Scenario: No notifications displayed if configuration is empty
     Given I have the configuration called 'config.yml'
       """
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

  Scenario: No notifications represented in JSON
    Given I have the configuration called 'config.yml'
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
    Given I have the configuration called 'config.yml'
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
          type: text
          update-with:
            name: text-from-message
            filter-messages:
              - type: message-matches-regex
                pattern: Hello
      """
    When I call 'view notifications config.yml'
    Then the status code is 0
    And the output is
      """
      {
          "notifications": [
              {
                  "filtered-messages": [
                      {
                          "source": "Text",
                          "text": "Hello"
                      }
                  ],
                  "notification-after": "Text notification (title=Display weather, text=Hello)",
                  "notification-before": "Text notification (title=Display weather, text=)"
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