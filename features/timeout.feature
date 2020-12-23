Feature: Test Ping Functionality
  @demo @XT-229
  Scenario: PING_EXPECTED_TRUE
    Given Nothing
    When I try to wait "10"
    Then I expect response "true"
