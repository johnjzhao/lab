#!/usr/bin/env python

from behave import *
import teradatasql
import pandas as pd
import os
import csv

host = "awstddev.sunvalle.net"
TDV_UNITTEST_USR = os.getenv('TDV_UNITTEST_USR')
TDV_UNITTEST_PSW = os.getenv('TDV_UNITTEST_PSW')
BUILD_NUMBER = os.getenv('BUILD_NUMBER')

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(CURRENT_DIR, 'test_data')
EXPECTED_DATA_DIR = os.path.join(CURRENT_DIR, 'expected_data')
TEST_DDL_DIR = os.path.join(CURRENT_DIR, 'test_ddl')

LANG_DIM_T13_datatypes = "(c1 varchar(3), c2 varchar(100), c3 integer, c4 integer)"
MBR_PH_DIM_T9_datatypes = "(c1 varchar(100), c2 varchar(100))"


@given('I have a TDV connection')
def step_impl(context):
    conn = teradatasql.connect(host=host, user=TDV_UNITTEST_USR, password=TDV_UNITTEST_PSW,logmech="LDAP",encryptdata="true")
    context.response = {}
    context.response['conn'] = conn


@when('I setup the following expected data')
def step_impl(context):
    for arg_dict in context.table:
        filename = arg_dict['expected_data_filename']
        num_cols = arg_dict['num_cols']
    expected_data_file = os.path.join(EXPECTED_DATA_DIR, filename)

    tablename = "voltab_expected_"+ str(BUILD_NUMBER)

    conn = context.response['conn']
    with conn.cursor () as cur:
        # Create a volatile table and insert expected results data into it
        if int(num_cols) == 4:
            cur.execute(f"create volatile table {tablename} {LANG_DIM_T13_datatypes} on commit preserve rows")
            cur.execute("{fn teradata_read_csv(%s)} insert into %s (?,?,?,?)" % (expected_data_file, tablename))
        
        else: # we are only have tests for two tables that have either 2 or 4 columns
            cur.execute(f"create volatile table {tablename} {MBR_PH_DIM_T9_datatypes} on commit preserve rows")
            cur.execute("{fn teradata_read_csv(%s)} insert into %s (?,?)" % (expected_data_file, tablename))

        cur.execute(f"select * from {tablename}")
        expected_data = pd.DataFrame(cur.fetchall())
        context.response['expected'] = expected_data


@when('I execute the SQL on the test data')
def step_impl(context):
    for arg_dict in context.table:
        data_filename = arg_dict['test_data_filename']
        ddl_filename = arg_dict['ddl_filename']
        tablename = arg_dict['test_data_tablename'] + "_"+ str(BUILD_NUMBER)
        num_cols = arg_dict['num_cols']
    test_data_file = os.path.join(TEST_DATA_DIR, data_filename)
    ddl_file = os.path.join(TEST_DDL_DIR, ddl_filename)
    with open(ddl_file, "r") as f:
        query = f.read()
    query= query.replace('tablename', tablename)


    conn = context.response['conn']
    with conn.cursor () as cur:
        # Create a volatile table and insert test data into it
        if int(num_cols) == 4:
            cur.execute(f"create volatile table {tablename} {LANG_DIM_T13_datatypes} on commit preserve rows")
            cur.execute("{fn teradata_read_csv(%s)} insert into %s (?,?,?,?)" % (test_data_file, tablename))

        else:
            cur.execute(f"create volatile table {tablename} {MBR_PH_DIM_T9_datatypes} on commit preserve rows")
            cur.execute("{fn teradata_read_csv(%s)} insert into %s (?,?)" % (test_data_file, tablename)) 

        cur.execute(query)
        test_data = pd.DataFrame(cur.fetchall())
        context.response['test'] = test_data


@then('I see that the result matches the expected')
def step_impl(context):
    if context.table: # expected result provided in feature.
        for arg_dict in context.table: 
            expected_result = arg_dict['expected_result']
            if arg_dict['result_type'] == 'int': # used to cast expected_result to int if needed (ex. query is select count(*))
                expected_result = int(expected_result)
        assert expected_result in context.response['test'].values
    else: # no expected_result provided in feature. use expected data volatile table
        assert context.response['expected'].equals(context.response['test'])
        
    context.response['conn'].close()
