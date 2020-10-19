'''
    Author: Kyle Simpson
    Description: Database utilities
'''

import sqlite3
from sqlite3 import Error

# This allows us to replace the sqlite3 default row processor with our own
# to handle more complex ways of returning results (such as returning an object
# where we can access columns by name)
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Create standard connection method to database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect('./gfatm_api/db_data/{}.db'.format(str(db_file)))
        conn.row_factory = dict_factory
        print('  Database found at ./gfatm_api/db_data/{}.db'.format(str(db_file)))
        return conn
    except Error as e:
        print(e)

    return conn


# Create desired table in the provided db connection
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print('  Table created successfully')
    except Error as e:
        print(e)


# Table updating code
def insert_into_table(conn, insert_sql):
    try:
        c = conn.cursor()
        c.execute(insert_sql)
        conn.commit()
    except Error as e:
        print(e)