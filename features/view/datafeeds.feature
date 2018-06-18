Feature: View output of data-feeds

    Scenario: Emtpy configuration causes error
     Given I have the configuration called 'config.yml'
        """
        """
     When I call 'view datafeeds config.yml'
     Then the status code is 1
     And the output is
        """
        Error reading configuration file 'config.yml':
        Configuration file is empty
        Aborted!

        """

  Scenario: No data-feeds represented in JSON
    Given I have the configuration called 'config.yml'
       """
       data-feeds:
       """
    When I call 'view datafeeds config.yml'
    Then the status code is 0
    And the output is
       """
       {
           "source-data": []
       }

       """

  Scenario: Single data-feed with single output represented in JSON
    Given I have the configuration called 'config.yml'
       """
       data-feeds:
         - source: text
           text: Test 1
       """
    When I call 'view datafeeds config.yml'
    Then the status code is 0
    And the output is
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

  Scenario: Single data-feed with multiple output represented in JSON
    Given I have the configuration called 'config.yml'
       """
       data-feeds:
         - source: text
           text:
            - Test 1
            - Test 2
       """
    When I call 'view datafeeds config.yml'
    Then the status code is 0
    And the output is
       """
       {
           "source-data": [
               {
                   "source": "Text",
                   "text": "Test 1"
               },
               {
                   "source": "Text",
                   "text": "Test 2"
               }
           ]
       }

       """

    Scenario: Multiple data-feed with one multiple output represented in JSON
    Given I have the configuration called 'config.yml'
       """
       data-feeds:
         - source: text
           text: Test 1
         - source: text
           text:
            - Test 2
            - Test 3
       """
    When I call 'view datafeeds config.yml'
    Then the status code is 0
    And the output is
       """
       {
           "source-data": [
               {
                   "source": "Text",
                   "text": "Test 1"
               },
               {
                   "source": "Text",
                   "text": "Test 2"
               },
               {
                   "source": "Text",
                   "text": "Test 3"
               }
           ]
       }

       """
