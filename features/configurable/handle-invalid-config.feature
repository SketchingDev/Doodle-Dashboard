Feature: User is informed of invalid dashboard configuration


  Scenario: Emtpy configuration causes error
    Given I have the configuration called 'config.yml'
      """
      """
    When I call 'start --once config.yml'
    Then the status code is 1
    And the output is
      """
      Error reading configuration file 'config.yml':
      Configuration file is empty
      Aborted!

      """

  Scenario: Malformed YAML causes error
    Given I have the configuration called 'config.yml'
      """
      :
      """
    When I call 'start --once config.yml'
    Then the status code is 1
    And the output is
      """
      Error parsing configuration file 'config.yml':
      while parsing a block mapping
      expected <block end>, but found ':'
        in "config.yml", line 1, column 1
      Aborted!

      """

  Scenario: Invalid data-feed causes error
    Given I have the configuration called 'config.yml'
       """
       data-feeds: testing
       """
    When I call 'start --once config.yml'
    Then the status code is 1
    And the output is
       """
       Error reading configuration file 'config.yml':
       No display defined. Check that the ID you provided is valid.
       Aborted!

       """