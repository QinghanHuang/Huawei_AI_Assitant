import os
import re
import json
import time
import numpy as np
import pandas as pd
import sqlite3
from io import StringIO 



def test_connect_fun(path):
    db = sqlite3.connect(path)
    return db

def sql_query_fun(sql_query, db):
    df = pd.read_sql_query(sql_query, db)
    return df


def test_query_fun(query, table_id, db, sql_query = None):
    if not sql_query:
        sql_query = query  # Wish me luck!
    df = sql_query_fun(sql_query, db)
    return df.to_string()


def run_test(test_name, connect_fun, query_fun):
    with open(test_name + ".json", "r") as test_file:
        test_cases = json.load(test_file)

    db = connect_fun(test_name + ".sqlite3")
    for test_case in test_cases:
        (f"Question: {test_case['question']}")
        if 'sql' in test_case and len(test_case['sql']):
            sql = test_case['sql'][0]
            print(f"Example query: {test_case['sql'][0]}")
        else:
            sql = None
        expected = pd.read_json(StringIO(test_case['sql_result']))
        print(f"Example result:")
        print(expected.to_string())
        
        if query_fun.__code__.co_argcount > 3:
            model_result = query_fun(test_case['question'], test_case['table_id'], db, sql)
        else:
            model_result = query_fun(test_case['question'], test_case['table_id'], db)
        print(f"Model result:")
        print(model_result)
        print()


if __name__ == '__main__':

    run_test('example-data/example-simple', test_connect_fun, test_query_fun)

