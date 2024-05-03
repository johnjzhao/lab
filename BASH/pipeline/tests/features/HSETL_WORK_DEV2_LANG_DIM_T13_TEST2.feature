#!/usr/bin/env python

Feature: SQL test - simple query
    Compare query result on test data with expected result

@example1
Scenario: project2/1.sql, validate a count(*) query by providing the expected_result
    Given I have a TDV connection
    When I setup the following expected data
        | expected_data_filename                    | num_cols |  
        | HSETL_WORK_DEV2_LANG_DIM_T13_EXPECTED.csv | 4        |  
    When I execute the SQL on the test data
        | test_data_filename                    | test_data_tablename       | ddl_filename                                 | num_cols |                 
        | HSETL_WORK_DEV2_LANG_DIM_T13_TEST.csv | LANG_DIM_T13_TEST         | HSETL_WORK_DEV2_LANG_DIM_T13_TEST_QUERY2.txt | 4        |  
    Then I see that the result matches the expected
        | expected_result | result_type     |
        | 10              | int             |