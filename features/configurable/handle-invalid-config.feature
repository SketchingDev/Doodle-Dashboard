Feature: User is informed of invalid dashboard configuration

  Scenario: Unknown display causes error
    Given I have the configuration called 'config.yml'
      """
      display: none
      """
    When I call 'start --once config.yml'
    Then the status code is 1
    And the output is
      """
      Cannot find the display 'none'. Have you run `pip install` for the display you're trying to use?
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
      Error while parsing a block mapping
      expected <block end>, but found ':'
        in "config.yml", line 1, column 1
      Aborted!

      """