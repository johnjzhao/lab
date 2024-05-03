#!/usr/bin/env python

Feature: SQL test - simple query
    Compare query result on test data with expected result

@example1
Scenario: project1/3.sql, validate query
    Given I have a TDV connection
    When I setup the following expected data
        | expected_data_filename                     | num_cols |  
        | HSETL_WORK_DEV2_MBR_PH_DIM_T9_EXPECTED.csv | 2        |  
    When I execute the SQL on the test data
        | test_data_filename                     | test_data_tablename      | ddl_filename                                 | num_cols |                        
        | HSETL_WORK_DEV2_MBR_PH_DIM_T9_TEST.csv | MBR_PH_DIM_T9_TEST       | HSETL_WORK_DEV2_MBR_PH_DIM_T9_TEST_QUERY.txt | 2        |  
    Then I see that the result matches the expected
